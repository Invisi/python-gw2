import functools

from gw2 import models

from ._base import Base, IdsBase


class Professions(IdsBase[models.Profession, str], _type=models.Profession):
    pass


class Profession(Base[models.Profession], _type=models.Profession):
    def __init__(self, profession_id: str):
        self.profession_id = profession_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"professions/{self.profession_id}"
