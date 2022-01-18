import functools
import logging
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)

import httpx
import pkg_resources  # type: ignore
from pydantic import ValidationError

from gw2 import errors
from gw2.utils import chunks

try:
    __version__ = pkg_resources.get_distribution("gw2").version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"

# Global config
BASE_URL = "https://api.guildwars2.com/v2"
DEFAULT_TIMEOUT = 10
SCHEMA = "2021-04-06T21:00:00.000Z"


LOG = logging.getLogger(__name__)

# The model for the endpoint
EndpointModel = TypeVar("EndpointModel")

# IDs on endpoints. May be integer or (e.g.) a character name
EndpointId = TypeVar("EndpointId", str, int)
IdsVariant = TypeVar("IdsVariant", str, int)
IdsParameter = Union[str, int, None]


def _create_session() -> httpx.AsyncClient:
    session = httpx.AsyncClient()

    # Set request headers
    session.headers.update(
        {
            "User-Agent": f"Invisi/python-gw2@{__version__}",
            "Accept": "application/json",
            "Accept-Language": "en",  # TODO: configurable
            "X-Schema-Version": SCHEMA,
        }
    )

    return session


class _Base(Generic[EndpointModel]):
    # Cache expiry, may be set on the endpoint itself
    expiry: Optional[int] = 5 * 60
    _types: Dict[str, Any] = {}

    def __init__(self) -> None:
        self._session = _create_session()

    def __init_subclass__(cls, _type: Optional[Any] = None):
        """
        Registers model class for later use in get()

        Args:
            _type: The model (data)class
        """

        super().__init_subclass__()

        if _type is not None:
            cls._types[f"{cls.__module__}.{cls.__name__}"] = _type

    @functools.cached_property
    def suffix(self) -> str:
        """
        Suffix for the base url, the class name is the default
        """

        return self.__class__.__name__.lower()

    @functools.cached_property
    def url(self) -> str:
        """
        Generates endpoint URL
        """

        return f"{BASE_URL}/{self.suffix}"

    def _cast(self, data: Dict[str, Any]) -> EndpointModel:
        """
        Casts data into model

        *May be overridden inside the model itself*
        """

        type_key = f"{self.__module__}.{self.__class__.__name__}"
        assert type_key in self._types, "Endpoint is missing type definition."

        klass = self._types[type_key]
        try:
            if isinstance(data, list):
                return cast(EndpointModel, klass(*data))
            elif isinstance(data, dict):
                return cast(EndpointModel, klass(**data))

            return cast(EndpointModel, klass(data))
        except (TypeError, ValidationError):
            LOG.exception("Failed to coerce data into model")
            raise NotImplementedError()

    # region _get()
    @overload
    async def _get(
        self,
        *,
        _id: IdsParameter,
        ids: None = None,
        _raw: Literal[True],
    ) -> Any:
        ...

    @overload
    async def _get(
        self,
        *,
        _id: IdsParameter,
        ids: None = None,
        _raw: Literal[False] = False,
    ) -> EndpointModel:
        ...

    @overload
    async def _get(
        self,
        *,
        _id: None = None,
        ids: List[IdsVariant],
        _raw: Literal[True],
    ) -> List[Any]:
        ...

    @overload
    async def _get(
        self, *, _id: None = None, ids: List[IdsVariant], _raw: Literal[False] = False
    ) -> List[EndpointModel]:
        ...

    @overload
    async def _get(
        self, *, _id: None = None, ids: None = None, _raw: Literal[True]
    ) -> Any:
        ...

    @overload
    async def _get(self) -> EndpointModel:
        ...

    async def _get(
        self,
        *,
        _id: IdsParameter = None,
        ids: Optional[List[IdsVariant]] = None,
        _raw: bool = False,
    ) -> Union[Any, EndpointModel, List[Any], List[EndpointModel]]:
        """
        Get model or raw value from endpoint

        Args:
            _raw: Return the raw API response instead of a model instance

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        # TODO: Check if authentication is required
        # TODO: Caching
        # TODO: https://pypi.org/project/asyncio-throttle/

        params: Dict[str, Union[IdsParameter, List[IdsVariant]]] = {}

        if _id is not None:
            params["id"] = _id

        if ids is not None:
            params["ids"] = ",".join(str(_) for _ in ids)

        try:
            response = await self._session.get(
                self.url, params=params, timeout=DEFAULT_TIMEOUT
            )
        except httpx.NetworkError:
            LOG.exception("Failed to fetch data")
            raise

        # Raise error if the key is reported as invalid
        if (
            400 <= response.status_code <= 403
            and "authorization" in self._session.headers
            and "invalid" in response.text.lower()
        ):
            raise errors.InvalidKeyError

        # 206 might be returned if only part of the ids were valid, for example
        if response.status_code == 200 or response.status_code == 206:
            if _raw:
                return response.json()

            if ids is None:
                return self._cast(response.json())
            else:
                return [self._cast(_data) for _data in response.json()]

        response.raise_for_status()

        # Raise again because mypy complains otherwise
        raise httpx.HTTPError("Unknown API error")

    # endregion _get()

    def auth(self, api_key: Optional[str] = None) -> None:
        """
        Add or remove API key to requests, this will be set globally

        Args:
            api_key: A (hopefully) valid API key
        """

        # Set key on session
        if api_key:
            self._session.headers.update({"Authorization": f"Bearer {api_key}"})
            return

        # Remove key from session
        if "authorization" in self._session.headers:
            del self._session.headers["authorization"]

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {self.url}>"


class Base(_Base[EndpointModel]):
    async def get(self) -> EndpointModel:
        return await self._get()


class ListBase(_Base[EndpointModel]):
    """
    Base class for endpoints that return a list of objects by default,
    like /account/achievements.
    """

    async def get(self) -> Union[List[EndpointModel]]:
        """
        Returns a list of models

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        # Do casting here since _get would otherwise try to do the casting
        # wrongly
        _ = cast(List[Dict[str, Any]], await super()._get(_raw=True))
        return [self._cast(_data) for _data in _]


class IdsBase(Generic[EndpointModel, EndpointId], _Base[EndpointModel]):
    """
    Base class for endpoints that return IDs (or names in case of the
    character endpoint) if requested without any special parameters.
    """

    async def ids(self) -> List[EndpointId]:
        """
        Returns a list of IDs for this endpoint
        """

        return cast(List[EndpointId], await super()._get(_raw=True))

    async def one(self, _id: EndpointId) -> EndpointModel:
        """
        Return a model for a given ID

        Args:
            _id: The id which should be retrieved
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """
        return cast(EndpointModel, await super()._get(_id=_id))

    async def many(self, ids: List[EndpointId]) -> AsyncIterator[EndpointModel]:
        """
        Returns an async generator for the requested objects

        Args:
            ids: A list of IDs. String or integer
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        for chunk in chunks(ids, 200):
            for _model in await self._get(ids=chunk):
                yield _model

    async def all(self) -> AsyncIterator[EndpointModel]:
        """
        Returns an async iterator for all objects on this endpoint

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        # TODO: Use ?ids=all on endpoints where that is supported

        # Grab all IDs
        ids = await self.ids()

        # Just throw them into many()
        return self.many(ids=ids)

    # TODO: Maybe add a .count property that pre-caches ids?
