import asyncio
import functools
import logging
from asyncio import Future, Task
from collections.abc import AsyncIterator
from importlib.metadata import PackageNotFoundError, version
from types import GenericAlias
from typing import (
    Any,
    Generic,
    Literal,
    Self,
    TypeVar,
    _GenericAlias,
    cast,
    overload,
)

import httpx
import pydantic
from asyncio_throttle import Throttler
from pydantic import ValidationError

from gw2 import errors
from gw2.utils import chunks

try:
    __version__ = version("gw2")
except PackageNotFoundError:
    __version__ = "unknown"

# Global config
BASE_URL = "https://api.guildwars2.com/v2"
DEFAULT_TIMEOUT = 10
SCHEMA = "2021-04-06T21:00:00.000Z"
# todo: schema per endpoint, assume the above as default.
#       could be implemented as another property

HTTP_SUCCESS = 200
HTTP_PARTIAL_SUCCESS = 206
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN = 403

GLOBAL_THROTTLE = Throttler(rate_limit=300, period=60)


# TODO: better rate limiting
#  https://github.com/greaka/gw2api/blob/ab5a08cec3004b3cea8a62b51b3831a097adb989/http/src/rate_limit.rs#L44-L66


LOG = logging.getLogger(__name__)

# The model for the endpoint
EndpointModel = TypeVar("EndpointModel")

# IDs on endpoints. May be integer or (e.g.) a character name
EndpointId = TypeVar("EndpointId", str, int)
IdsVariant = TypeVar("IdsVariant", str, int)
IdsParameter = str | int | None


def _create_session(timeout: float) -> httpx.AsyncClient:
    session = httpx.AsyncClient(timeout=timeout)

    # Set request headers
    session.headers.update(
        {
            "User-Agent": f"Invisi/python-gw2@{__version__}",
            "Accept": "application/json",
            "Accept-Language": "en",  # TODO: configurable
            "X-Schema-Version": SCHEMA,
        },
    )

    return session


class _Base(Generic[EndpointModel]):
    # Cache expiry, may be set on the endpoint itself
    expiry: int | None = 5 * 60
    _ids_params: dict[str, str] = {}

    # Optional global default API key
    _api_key: str | None

    def __init__(self, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._session = _create_session(timeout)

        self.api_key: None | str = None

        # Set API key from global storage
        if hasattr(type(self), "_api_key"):
            self.auth(type(self)._api_key)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: Any = None,
    ) -> None:
        """
        Closes the httpx session properly
        """

        await self._session.aclose()

    @functools.cached_property
    def suffix(self) -> str:
        """
        Suffix for the base url, the class name is the default
        """

        return self.__class__.__name__.lower()

    @functools.cached_property
    def url(self) -> str:
        """Generates endpoint URL"""

        return f"{BASE_URL}/{self.suffix}"

    @functools.cached_property
    def _klass(self) -> EndpointModel:
        """
        Returns the actual endpoint model instance for later use, can be a
        `str`, `int`, list[BaseModel], or anything similar
        """
        try:
            generic_alias = next(
                filter(
                    lambda x: isinstance(x, _GenericAlias | GenericAlias),
                    self.__orig_bases__,
                )
            )
        except StopIteration as e:
            raise NotImplementedError from e

        if issubclass(self.__class__, IdsBase | ListBase | StringsBase):
            return cast(EndpointModel, list[generic_alias.__args__[0]])
        elif issubclass(self.__class__, Base):
            return cast(EndpointModel, generic_alias.__args__[0])
        else:
            raise NotImplementedError

    def _cast(self, data: dict[str, Any] | list | str) -> EndpointModel:
        """
        Casts data into model

        *May be overridden inside the model itself*
        """

        try:
            if isinstance(data, str):
                return pydantic.TypeAdapter(self._klass).validate_json(data)

            return pydantic.TypeAdapter(self._klass).validate_python(data)
        except (TypeError, ValueError, ValidationError) as e:
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
    ) -> str:
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
        ids: list[IdsVariant] | Literal["all"],
        _raw: Literal[True],
    ) -> str:
        ...

    @overload
    async def _get(
        self,
        *,
        _id: None = None,
        ids: list[IdsVariant] | Literal["all"],
        _raw: Literal[False] = False,
    ) -> list[EndpointModel]:
        ...

    @overload
    async def _get(
        self,
        *,
        _id: None = None,
        ids: None = None,
        _raw: Literal[True],
    ) -> str:
        ...

    @overload
    async def _get(self) -> EndpointModel:
        ...

    async def _get(
        self,
        *,
        _id: IdsParameter = None,
        ids: list[IdsVariant] | Literal["all"] | None = None,
        _raw: bool = False,
    ) -> str | EndpointModel | list[EndpointModel]:
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

        params: dict[str, IdsParameter | list[IdsVariant]] = self._params.copy()

        if _id is not None:
            params["id"] = _id

        if ids is not None:
            ids_name = self._ids_params.get(
                f"{self.__module__}.{self.__class__.__name__}",
                "ids",
            )

            if isinstance(ids, list):
                params[ids_name] = ",".join(str(_) for _ in ids)
            elif ids == "all":
                params[ids_name] = "all"

        LOG.debug("Sending request to %s with params %s", self.url, params)
        async with GLOBAL_THROTTLE:
            try:
                response = await self._session.get(self.url, params=params)
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
        if response.status_code in {HTTP_SUCCESS, HTTP_PARTIAL_SUCCESS}:
            if _raw:
                return response.text

            return self._cast(response.text)

        LOG.debug(
            "Unhandled HTTP response: status=%s content=%s",
            response.status_code,
            response.text,
        )
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

    @functools.cached_property
    def _params(self) -> dict:
        """
        Allows injecting custom parameters into requests, e.g. for recipe or
        guild search
        """

        return {}

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

    async def get(self) -> list[EndpointModel]:
        """
        Returns a list of models

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        raw_data = await super()._get(_raw=True)
        return pydantic.TypeAdapter(list[EndpointModel]).validate_json(raw_data)


class StringsBase(_Base[EndpointModel]):
    """
    Base class for endpoints that return a list of strings by default,
    like /dailycrafting or /dungeons.
    """

    async def get(self) -> list[str]:
        """
        Returns a list of strings

        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        raw_data = await super()._get(_raw=True)
        return pydantic.TypeAdapter(list[str]).validate_json(raw_data)


class IdsBase(Generic[EndpointModel, EndpointId], _Base[EndpointModel]):
    """
    Base class for endpoints that return IDs (or names in case of the
    character endpoint) if requested without any special parameters.
    """

    async def ids(self) -> list[EndpointId]:
        """
        Returns a list of IDs for this endpoint
        """

        data = await super()._get(_raw=True)
        return pydantic.TypeAdapter(list[EndpointId]).validate_json(data)

    async def one(self, _id: EndpointId) -> EndpointModel:
        """
        Return a model for a given ID

        Args:
            _id: The id which should be retrieved
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """
        return cast(EndpointModel, await super()._get(_id=_id))

    async def many(
        self,
        ids: list[EndpointId] | Literal["all"],
        *,
        concurrent: bool = False,
    ) -> AsyncIterator[EndpointModel]:
        """
        Returns an async generator for the requested objects

        Args:
            ids: A list of IDs or "all"
            concurrent: Enable concurrent requests. Will wait for all requests to finish
                        before the iterator becomes available.
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        if ids == "all":
            for _model in await self._get(ids="all"):
                yield _model

            return

        if concurrent:
            tasks: list[Task] = []
            for chunk in chunks(ids, 200):
                tasks.append(asyncio.ensure_future(self._get(ids=chunk)))

            for results in await cast(
                Future[list[list[EndpointModel]]],
                asyncio.gather(*tasks),
            ):
                for _model in cast(list[EndpointModel], results):
                    yield _model
        else:
            for chunk in chunks(ids, 200):
                for _model in await self._get(ids=chunk):
                    yield _model

    async def all(self, *, concurrent: bool = False) -> AsyncIterator[EndpointModel]:
        """
        Returns an async iterator for all objects on this endpoint

        Args:
            concurrent: Enable concurrent requests. Will wait for all requests to finish
                        before the iterator becomes available.
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        # Grab all IDs
        ids = await self.ids()

        # Just throw them into many()
        async for _ in self.many(ids=ids, concurrent=concurrent):
            yield _

    async def all_noniter(self, *, concurrent: bool = False) -> list[EndpointModel]:
        """
        Returns a list of all objects on this endpoint

        Args:
            concurrent: Enable concurrent requests. Will wait for all requests to finish
                        before the iterator becomes available.
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
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
        async for item in self.many(ids=ids, concurrent=concurrent):
            items.append(item)

        return items

    # TODO: Maybe add a .count property that pre-caches ids?

    def __init_subclass__(cls, _ids_param: str | None = None):
        """
        - Registers ids parameter for later use, defaults to "ids"
        - Registers model class for later use in get()

        Args:
            _ids_param: The query parameter for `ids`
        """

        super().__init_subclass__()

        if _ids_param is not None:
            cls._ids_params[f"{cls.__module__}.{cls.__name__}"] = _ids_param


class AllIdsBase(
    Generic[EndpointModel, EndpointId], IdsBase[EndpointModel, EndpointId]
):
    """
    Base class for endpoints that return IDs (or names in case of the
    character endpoint) if requested without any special parameters and ?ids=all.
    """

    # TODO: Use ?ids=all on endpoints where that is supported

    async def all(self, *, concurrent: bool = False) -> AsyncIterator[EndpointModel]:
        """
        Returns an async iterator for all objects on this endpoint

        Args:
            concurrent: Doesn't do anything. See Liskov Substitution Principle.
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        async for _ in self.many(ids="all"):
            yield _

    async def all_noniter(self, *, concurrent: bool = False) -> list[EndpointModel]:
        """
        Returns a list of all objects on this endpoint

        Args:
            concurrent: Doesn't do anything. See Liskov Substitution Principle.
        Raises:
             httpx.NetworkError: Network-related issues, should not be hit
                                 usually
             httpx.HTTPError: The server responded with a 4xx or 5xx, and
                              it's not because of an invalid API key
             InvalidKeyError: The API reported that the currently used API key
                            is invalid. This may be caused by invalid keys or
                            server-side caching issues.
             NotImplementedError: Should never occur but might if the API
                                  response changes in unexpected ways.
        """

        items = []
        async for item in self.many(ids="all"):
            items.append(item)

        return items
