import functools

from gw2 import models

from .._base import Base, IdsBase


class Achievements(IdsBase[models.Achievement, int], _type=models.Achievement):
    pass


class Achievement(Base[models.Achievement], _type=models.Achievement):
    def __init__(self, achievement_id: int):
        self.achievement_id = achievement_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/{self.achievement_id}"
