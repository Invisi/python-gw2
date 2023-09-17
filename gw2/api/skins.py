import functools

from gw2 import models

from ._base import Base, IdsBase


class Skins(IdsBase[models.Skin, int]):
    pass


class Skin(Base[models.Skin]):
    def __init__(self, skin_id: int):
        self.skin_id = skin_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"skins/{self.skin_id}"
