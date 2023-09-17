import functools

import pydantic

from gw2 import errors

from ..models import guild
from ._base import Base, IdsBase, StringsBase


class _Guild:
    def __init__(self, guild_id: str):
        self.guild_id = guild_id
        super().__init__()


class Guild(
    _Guild,
    Base[guild.Guild | guild.AuthenticatedGuild],
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}"


class GuildSearch(Base[guild.Guild]):
    suffix = "guild/search"

    def __init__(self, name: str):
        self.name = name
        super().__init__()

    @functools.cached_property
    def _params(self) -> dict:
        return {"name": self.name}

    async def ids(self) -> list[str]:
        raw_data = await super()._get(_raw=True)
        return pydantic.TypeAdapter(list[str]).validate_json(raw_data)

    async def get(self) -> guild.Guild:
        guids = await self.ids()
        if len(guids) == 0:
            raise errors.GuildNotFoundError()

        return await Guild(guids[0]).get()


class GuildPermissions(StringsBase[guild.GuildPermission]):
    suffix = "guild/permissions"


class GuildPermission(Base[guild.GuildPermission]):
    def __init__(self, permission_id: str):
        self.permission_id = permission_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/permissions/{self.permission_id}"


class GuildUpgrades(IdsBase[guild.GuildUpgrade, int]):
    suffix = "guild/upgrades"


class GuildUpgrade(Base[guild.GuildUpgrade]):
    def __init__(self, upgrade_id: int):
        self.upgrade_id = upgrade_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/upgrades/{self.upgrade_id}"
