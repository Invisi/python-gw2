import functools

from gw2 import models

from ._base import Base, StringsBase


class WorldBosses(StringsBase[models.WorldBoss], _type=models.WorldBoss):
    pass


class WorldBoss(Base[models.WorldBoss], _type=models.WorldBoss):
    def __init__(self, boss_id: str):
        self.boss_id = boss_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"worldbosses/{self.boss_id}"
