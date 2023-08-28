import functools

from gw2 import models

from ._base import Base, IdsBase


class MapChests(IdsBase[models.MapChest, int], _type=models.MapChest):
    pass


class MapChest(Base[models.MapChest], _type=models.MapChest):
    def __init__(self, map_chest: str):
        self.map_chest = map_chest
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"mapchests/{self.map_chest}"
