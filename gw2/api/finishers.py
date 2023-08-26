import functools

from gw2 import models

from ._base import Base, IdsBase


class Finishers(IdsBase[models.Finisher, int], _type=models.Finisher):
    pass


class Finisher(Base[models.Finisher], _type=models.Finisher):
    def __init__(self, finisher_id: int):
        self.finisher_id = finisher_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"finishers/{self.finisher_id}"
