import functools
import logging
from typing import (
    Any,
    AsyncGenerator,
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
import pkg_resources

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
    # Optional suffix for the base url, the class name is the default
    suffix: Optional[str] = None

    # Cache expiry, may be set on the endpoint itself
    expiry: Optional[int] = 5 * 60

    _session = _create_session()
    _types: Dict[str, Any] = {}

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
    def url(self) -> str:
        """
        Generates endpoint URL
        """

        if self.suffix is not None:
            return f"{BASE_URL}/{self.suffix}"

        return f"{BASE_URL}/{self.__class__.__name__.lower()}"

    def cast(self, data: Dict[str, Any]) -> EndpointModel:
        """
        Casts data into model
        """

        type_key = f"{self.__module__}.{self.__class__.__name__}"
        assert type_key in self._types, "Endpoint is missing type definition."

        return cast(EndpointModel, self._types[type_key](**data))

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
             httpx.HTTPStatusError: The server responded with a 4xx or 5xx and
                                    it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
        """

        # TODO: Check if authentication is required
        # TODO: Caching
        # TODO: https://pypi.org/project/asyncio-throttle/

        params: Dict[str, Union[IdsParameter, List[IdsVariant]]] = {}

        if _id is not None:
            params["id"] = _id

        if ids is not None:
            params["ids"] = ids

        try:
            response = await self._session.get(
                self.url, params=params, timeout=DEFAULT_TIMEOUT
            )
        except httpx.NetworkError:
            LOG.exception("Failed to fetch data")
            raise

        # Raise error if the key is reported as invalid
        if (
            response.status_code in [400, 403]
            and "authentication" in self._session.headers
            and "invalid" in response.text.lower()
        ):
            raise errors.InvalidKeyError

        # 206 might be returned if only part of the ids were valid, for example
        if response.status_code == 200 or response.status_code == 206:
            if _raw:
                return response.json()

            if ids is None:
                return self.cast(response.json())
            else:
                return [self.cast(_data) for _data in response.json()]

        response.raise_for_status()

        # Raise again because mypy complains otherwise
        raise httpx.HTTPStatusError

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
    @overload
    async def get(self, *, _raw: Literal[True]) -> Any:
        ...

    @overload
    async def get(self) -> EndpointModel:
        ...

    async def get(self, *, _raw: bool = False) -> Union[Any, EndpointModel]:
        if _raw:
            return await self._get(_raw=True)
        return await self._get()


class ListBase(_Base[EndpointModel]):
    """
    Base class for endpoints that return a list of objects by default,
    like /account/achievements.
    """

    @overload
    async def get(self, _id: None = None, *, _raw: Literal[True]) -> List[Any]:
        ...

    @overload
    async def get(
        self, _id: None = None, *, _raw: Literal[False] = False
    ) -> List[EndpointModel]:
        ...

    @overload
    async def get(self, _id: Union[str, int], *, _raw: Literal[True]) -> Any:
        ...

    @overload
    async def get(
        self, _id: Union[str, int], *, _raw: Literal[False] = False
    ) -> EndpointModel:
        ...

    async def get(
        self, _id: IdsParameter = None, *, _raw: bool = False
    ) -> Union[EndpointModel, List[EndpointModel], Any, List[Any]]:
        data = await super()._get(_id=_id, _raw=True)

        if _id is None:
            if _raw is True:
                return cast(List[Any], data)

            return [self.cast(_data) for _data in data]
        else:
            if _raw is True:
                return cast(Any, data)

            return self.cast(data)

