import functools

from gw2 import models

from ._base import Base, IdsBase


class Pets(IdsBase[models.Pet, int], _type=models.Pet):
    pass


class Pet(Base[models.Pet], _type=models.Pet):
    def __init__(self, pet_id: int):
        self.pet_id = pet_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pets/{self.pet_id}"
