import functools

from gw2 import models
from gw2.api._base import Base, IdsBase


class GuildUpgrades(IdsBase[models.GuildUpgrade, int], _type=models.GuildUpgrade):
    suffix = "guild/upgrades"


class GuildUpgrade(Base[models.Guild], _type=models.Guild):
    def __init__(self, guild_id: str):
        self.guild_id = guild_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/upgrades/{self.guild_id}"
