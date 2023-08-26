import functools

from gw2 import models

from ._base import Base, IdsBase


class Traits(IdsBase[models.Recipe, int], _type=models.Trait):
    pass


class Trait(Base[models.Trait], _type=models.Trait):
    def __init__(self, trait_id: int):
        self.trait_id = trait_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"traits/{self.trait_id}"
