import functools

from gw2 import models

from ._base import Base, IdsBase


class Colors(IdsBase[models.Color, int], _type=models.Color):
    pass


class Color(Base[models.Color], _type=models.Color):
    def __init__(self, color_id: int):
        self.color_id = color_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"colors/{self.color_id}"
