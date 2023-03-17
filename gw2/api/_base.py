import functools
import logging
from collections.abc import AsyncIterator
from typing import Any, Generic, Literal, TypeVar, cast, overload

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

HTTP_SUCCESS = 200
HTTP_PARTIAL_SUCCESS = 206
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403

LOG = logging.getLogger(__name__)

# The model for the endpoint
EndpointModel = TypeVar("EndpointModel")

# IDs on endpoints. May be integer or (e.g.) a character name
EndpointId = TypeVar("EndpointId", str, int)
IdsVariant = TypeVar("IdsVariant", str, int)
IdsParameter = str | int | None


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
    expiry: int | None = 5 * 60
    _types: dict[str, Any] = {}

    # Optional global default API key
    _api_key: str | None

    def __init__(self) -> None:
        self._session = _create_session()

        self.api_key: None | str = None

        # Set API key from global storage
        if hasattr(type(self), "_api_key"):
            self.auth(type(self)._api_key)

    async def __aexit__(
        self,
        exc_type: None | type[BaseException] = None,
        exc_value: None | BaseException = None,
        traceback: Any = None,
    ) -> None:
        """
        Closes the httpx session properly
        """

        await self._session.aclose()

    def __init_subclass__(cls, _type: Any | None = None):
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

    def _cast(self, data: dict[str, Any]) -> EndpointModel:
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
        except (TypeError, ValidationError) as e:
            LOG.exception("Failed to coerce data into model: %s", data)
            raise NotImplementedError() from e

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
        ids: list[IdsVariant],
        _raw: Literal[True],
    ) -> list[Any]:
        ...

    @overload
    async def _get(
        self, *, _id: None = None, ids: list[IdsVariant], _raw: Literal[False] = False
    ) -> list[EndpointModel]:
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
        ids: list[IdsVariant] | None = None,
        _raw: bool = False,
    ) -> Any | EndpointModel | list[Any] | list[EndpointModel]:
        """
        Get model or raw value from endpoint

        Args:
            _raw: Return the raw API response instead of a model instance

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             httpx.ReadTimeout: The server did not respond in time, subclass of
                                HTTPError
             InvalidKeyError: The API reported that the currently used API key
                              is invalid. This may be caused by invalid keys or
                              server-side caching issues.
             MissingGameAccessError: The API reports this account as not having
                                     access to the game.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        # TODO: Check if authentication is required
        # TODO: Caching
        # TODO: https://pypi.org/project/asyncio-throttle/

        params: dict[str, IdsParameter | list[IdsVariant]] = {}

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
            HTTP_BAD_REQUEST <= response.status_code <= HTTP_FORBIDDEN
            and "authorization" in self._session.headers
            and "invalid" in response.text.lower()
        ):
            raise errors.InvalidKeyError

        if (
            response.status_code == HTTP_BAD_REQUEST
            and "account does not have game access" in response.text.lower()
        ):
            raise errors.MissingGameAccessError

        # 206 might be returned if only part of the ids were valid, for example
        if (
            response.status_code == HTTP_SUCCESS
            or response.status_code == HTTP_PARTIAL_SUCCESS
        ):
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

    def auth(self, api_key: str | None = None) -> None:
        """
        Add to or remove API key from requests

        Args:
            api_key: A (hopefully) valid API key
        """

        self.api_key = api_key

        # Set key on session
        if api_key:
            self._session.headers.update({"Authorization": f"Bearer {api_key}"})
            return

        # Remove key from session
        if "authorization" in self._session.headers:
            del self._session.headers["authorization"]

    def global_auth(self, api_key: str | None = None) -> None:
        """
        Add to or remove API key from, this will be set globally and is
        **not** thread-safe.

        All new instances will use this as the default API key,
        which may still be overridden via :py:function:`auth()`.

        Args:
            api_key: A (hopefully) value API key
        """

        # Register key globally
        _Base._api_key = api_key

        # Register key on the local instance as well
        self.auth(api_key)

    def __repr__(self) -> str:
        return f"<{self.__module__}.{self.__class__.__name__}: {self.url}>"


class Base(_Base[EndpointModel]):
    async def get(self) -> EndpointModel:
        return await self._get()

    async def __aenter__(self) -> "Base[EndpointModel]":
        return self


class ListBase(_Base[EndpointModel]):
    """
    Base class for endpoints that return a list of objects by default,
    like /account/achievements.
    """

    async def get(self) -> list[EndpointModel]:
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
        _ = cast(list[dict[str, Any]], await super()._get(_raw=True))
        return [self._cast(_data) for _data in _]

    async def __aenter__(self) -> "ListBase[EndpointModel]":
        return self


class IdsBase(Generic[EndpointModel, EndpointId], _Base[EndpointModel]):
    """
    Base class for endpoints that return IDs (or names in case of the
    character endpoint) if requested without any special parameters.
    """

    async def ids(self) -> list[EndpointId]:
        """
        Returns a list of IDs for this endpoint
        """

        return cast(list[EndpointId], await super()._get(_raw=True))

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

    async def many(self, ids: list[EndpointId]) -> AsyncIterator[EndpointModel]:
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

    async def all_noniter(self) -> list[EndpointModel]:
        """
        Returns a list of all objects on this endpoint

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

        # Grab all IDs
        ids = await self.ids()

        items = []
        async for item in self.many(ids=ids):
            items.append(item)

        return items

    # TODO: Maybe add a .count property that pre-caches ids?

    async def __aenter__(self) -> "IdsBase[EndpointModel, EndpointId]":
        return self
