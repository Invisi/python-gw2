import functools
from typing import Coroutine, cast

from gw2 import errors, models

from .._base import Base


class Guild(Base[models.Guild], _type=models.Guild):
    def __init__(self, guild_id: str):
        self.guild_id = guild_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}"


class GuildSearch(Base[models.Guild], _type=models.Guild):
    suffix = "guild/search"

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    @functools.cached_property
    def _params(self) -> dict:
        return {"name": self.name}

    async def ids(self) -> list[str]:
        return cast(list[str], await super()._get(_raw=True))

    async def get(self) -> models.Guild:
        guids = await self.ids()
        if len(guids) == 0:
            raise errors.GuildNotFoundError()

        return await Guild(guids[0]).get()
