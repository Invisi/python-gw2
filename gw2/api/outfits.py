import functools

from gw2 import models

from ._base import Base, IdsBase


class Outfits(IdsBase[models.Outfit, int]):
    pass


class Outfit(Base[models.Outfit]):
    def __init__(self, outfit_id: int):
        self.outfit_id = outfit_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"outfits/{self.outfit_id}"
