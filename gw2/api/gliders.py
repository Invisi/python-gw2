import functools

from gw2 import models

from ._base import Base, IdsBase


class Gliders(IdsBase[models.Glider, int], _type=models.Glider):
    pass


class Glider(Base[models.Glider], _type=models.Glider):
    def __init__(self, glider_id: int):
        self.glider_id = glider_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"gliders/{self.glider_id}"
