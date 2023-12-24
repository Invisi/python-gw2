import functools

import pydantic

from gw2 import errors

from ..models import guild
from ._base import Base, IdsBase, ListBase, StringsBase


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

    def log(self) -> "Log":
        client = Log(self.guild_id)
        client.auth(self.api_key)
        return client

    def members(self) -> "Members":
        client = Members(self.guild_id)
        client.auth(self.api_key)
        return client

    def ranks(self) -> "Ranks":
        client = Ranks(self.guild_id)
        client.auth(self.api_key)
        return client

    def stash(self) -> "Stash":
        client = Stash(self.guild_id)
        client.auth(self.api_key)
        return client

    def storage(self) -> "Storage":
        client = Storage(self.guild_id)
        client.auth(self.api_key)
        return client

    def teams(self) -> "Teams":
        client = Teams(self.guild_id)
        client.auth(self.api_key)
        return client

    def treasury(self) -> "Treasury":
        client = Treasury(self.guild_id)
        client.auth(self.api_key)
        return client

    def upgrades(self) -> "Upgrades":
        client = Upgrades(self.guild_id)
        client.auth(self.api_key)
        return client


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


class Log(
    _Guild,
    ListBase[
        guild.Log.Invite
        | guild.Log.InviteDeclined
        | guild.Log.Kick
        | guild.Log.Join
        | guild.Log.Motd
        | guild.Log.RankChange
        | guild.Log.Stash
        | guild.Log.Treasury
        | guild.Log.Upgrade
        | guild.Log.Influence
    ],
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/log"


class Members(_Guild, ListBase[guild.Member]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/members"


class Ranks(_Guild, ListBase[guild.Rank]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/ranks"


class Stash(_Guild, ListBase[guild.Stash]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/stash"


class Storage(_Guild, ListBase[guild.Storage]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/storage"


class Teams(_Guild, ListBase[guild.Team]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/teams"


class Treasury(_Guild, ListBase[guild.Treasury]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/treasury"


class Upgrades(_Guild, ListBase[int]):
    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}/upgrades"
