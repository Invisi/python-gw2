import functools

from gw2 import models

from ._base import Base, IdsBase


class Masteries(IdsBase[models.Mastery, int], _type=models.Mastery):
    pass


class Mastery(Base[models.Mastery], _type=models.Mastery):
    def __init__(self, mastery_id: int):
        self.mastery_id = mastery_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"masteries/{self.mastery_id}"
