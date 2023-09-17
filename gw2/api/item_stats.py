import functools

from gw2 import models

from ._base import Base, IdsBase


class ItemStats(IdsBase[models.ItemStat, str]):
    pass


class ItemStat(Base[models.ItemStat]):
    def __init__(self, stat_id: int):
        self.stat_id = stat_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"itemstats/{self.stat_id}"
