"""
https://en.gw2treasures.com/dev/api
"""

import asyncio
import functools
import logging
from asyncio import Future, Task
from typing import AsyncIterator, Literal, cast

import httpx
from asyncio_throttle import Throttler

from gw2 import errors, models
from gw2.const import HTTP_UNAUTHORIZED
from gw2.utils import get_generic_alias

# noinspection PyProtectedMember
from ..api._base import (
    DEFAULT_TIMEOUT,
    HTTP_SUCCESS,
    Base,
    EndpointId,
    EndpointModel,
    IdsBase,
    IdsParameter,
    _Base,
)

BASE_URL = "https://api.gw2treasures.com"
LOG = logging.getLogger(__name__)
GLOBAL_THROTTLE = Throttler(rate_limit=600, period=60)

__all__ = [
    "Achievements",
    "Achievement",
    "Items",
    "Item",
]


class _TBase(_Base[EndpointModel]):
    def __init__(self, api_key: str, timeout: float = DEFAULT_TIMEOUT):
        super().__init__(timeout)
        self.auth(api_key)

    @functools.cached_property
    def _klass(self) -> EndpointModel | list[EndpointModel]:
        """
        Returns the actual endpoint model instance for later use, can be a
        `str`, `int`, list[BaseModel], or anything similar
        """
        try:
            generic_alias = get_generic_alias(self)
        except StopIteration as e:
            raise NotImplementedError from e

        if issubclass(self.__class__, TIdsBase):
            return cast(
                EndpointModel,
                generic_alias.__args__[0],
            )
        elif issubclass(self.__class__, TBase):
            return cast(EndpointModel, generic_alias.__args__[0])
        else:
            raise NotImplementedError

    async def _get(  # type: ignore[override]
        self,
        *,
        _id: IdsParameter = None,
        ids: None = None,
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

        if ids is not None:
            raise NotImplementedError()

        if _id is not None:
            url = f"{self.url}/{_id}/data"
        else:
            url = self.url

        params = self._params.copy()
        LOG.debug("Sending request to %s with params %s", self.url, params)

        async with GLOBAL_THROTTLE:
            try:
                response = await self._session.get(url, params=params)
            except httpx.NetworkError:
                LOG.exception("Failed to fetch data")
                raise

        if response.status_code == HTTP_UNAUTHORIZED:
            raise errors.InvalidKeyError

        if response.status_code != HTTP_SUCCESS:
            response.raise_for_status()
            LOG.debug(
                "Unhandled HTTP response: status=%s content=%s",
                response.status_code,
                response.text,
            )

        if _raw:
            return response.text

        return self._cast(response.text)

    @functools.cached_property
    def url(self) -> str:
        """Generates endpoint URL"""

        return f"{BASE_URL}/{self.suffix}"


class TIdsBase(IdsBase[EndpointModel, EndpointId], _TBase[EndpointModel]):
    async def many(
        self,
        ids: list[EndpointId] | Literal["all"],
        *,
        concurrent: bool = False,
    ) -> AsyncIterator[EndpointModel]:
        if ids == "all":
            raise NotImplementedError()

        if concurrent:
            tasks: list[Task] = []
            for _id in ids:
                tasks.append(asyncio.ensure_future(self._get(_id=_id)))

            for _model in await cast(
                Future[list[EndpointModel]],
                asyncio.gather(*tasks),
            ):
                yield _model
        else:
            for _id in ids:
                yield cast(EndpointModel, await self._get(_id=_id))


class TBase(Base[EndpointModel], _TBase[EndpointModel]):
    pass


class Achievements(TIdsBase[models.Achievement, int]):
    pass


class Achievement(TBase[models.Achievement]):
    def __init__(
        self,
        api_key: str,
        achievement_id: int,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.achievement_id = achievement_id
        super().__init__(api_key=api_key, timeout=timeout)

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/{self.achievement_id}/data"


class Items(TIdsBase[models.Item, int]):
    # todo: implement filters
    pass


class Item(TBase[models.Item]):
    def __init__(
        self,
        api_key: str,
        item_id: int,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self.item_id = item_id
        super().__init__(api_key=api_key, timeout=timeout)

    @functools.cached_property
    def suffix(self) -> str:
        return f"items/{self.item_id}/data"
