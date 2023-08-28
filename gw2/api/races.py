import functools

from gw2 import models

from ._base import Base, StringsBase


class Races(StringsBase[models.Race], _type=models.Race):
    pass


class Race(Base[models.Race], _type=models.Race):
    def __init__(self, race_id: str):
        self.race_id = race_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"races/{self.race_id}"
