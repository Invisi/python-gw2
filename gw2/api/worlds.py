import functools

from gw2 import models

from ._base import Base, IdsBase


class Worlds(IdsBase[models.World, int]):
    pass


class World(Base[models.World]):
    def __init__(self, world_id: int):
        self.world_id = world_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"worlds/{self.world_id}"
