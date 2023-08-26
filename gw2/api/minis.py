import functools

from gw2 import models

from ._base import Base, IdsBase


class Minis(IdsBase[models.Mini, int], _type=models.Mini):
    pass


class Mini(Base[models.Mini], _type=models.Mini):
    def __init__(self, mini_id: int):
        self.mini_id = mini_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"minis/{self.mini_id}"
