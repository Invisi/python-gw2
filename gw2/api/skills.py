import functools

from gw2 import models

from ._base import Base, IdsBase


class Skills(IdsBase[models.Skill, int]):
    pass


class Skill(Base[models.Skill]):
    def __init__(self, skill_id: int):
        self.skill_id = skill_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"skills/{self.skill_id}"
