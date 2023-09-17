import functools
from typing import cast

from gw2 import errors, models

from ._base import Base, IdsBase, StringsBase


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


class GuildPermissions(
    StringsBase[models.GuildPermission], _type=models.GuildPermission
):
    suffix = "guild/permissions"


class GuildPermission(Base[models.GuildPermission], _type=models.GuildPermission):
    def __init__(self, permission_id: str):
        self.permission_id = permission_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/permissions/{self.permission_id}"


class GuildUpgrades(IdsBase[models.GuildUpgrade, int], _type=models.GuildUpgrade):
    suffix = "guild/upgrades"


class GuildUpgrade(Base[models.GuildUpgrade], _type=models.GuildUpgrade):
    def __init__(self, upgrade_id: int):
        self.upgrade_id = upgrade_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/upgrades/{self.upgrade_id}"
