import functools

from gw2 import models
from gw2.api._base import Base, IdsBase


class Characters(IdsBase[models.Character, str], _type=models.Character):
    pass


class Character(Base[models.Character], _type=models.Character):
    def __init__(self, character_name: str):
        self.character_name = character_name

    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}"
