import functools

from gw2 import models

from ._base import Base, IdsBase


class Maps(IdsBase[models.Map, int]):
    pass


class Map(Base[models.Map]):
    def __init__(self, map_id: int):
        self.map_id = map_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"maps/{self.map_id}"
