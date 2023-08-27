import functools

from gw2 import models

from .._base import Base, IdsBase


class GuildUpgrades(IdsBase[models.GuildUpgrade, int], _type=models.GuildUpgrade):
    suffix = "guild/upgrades"


class GuildUpgrade(Base[models.GuildUpgrade], _type=models.GuildUpgrade):
    def __init__(self, upgrade_id: int):
        self.upgrade_id = upgrade_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/upgrades/{self.upgrade_id}"
