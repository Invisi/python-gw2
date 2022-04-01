import functools
from typing import List

from gw2 import models
from gw2.api._base import Base, IdsBase, ListBase
from gw2.models import characters


class Characters(IdsBase[models.Character, str], _type=models.Character):
    pass


class _Character:
    def __init__(self, character_name: str):
        self.character_name = character_name
        super().__init__()


class Character(_Character, Base[models.Character], _type=models.Character):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}"

    def backstory(self) -> "Backstory":
        client = Backstory(self.character_name)
        client.auth(self.api_key)
        return client

    def core(self) -> "Core":
        client = Core(self.character_name)
        client.auth(self.api_key)
        return client

    def crafting(self) -> "Crafting":
        client = Crafting(self.character_name)
        client.auth(self.api_key)
        return client

    def equipment(self) -> "Equipment":
        client = Equipment(self.character_name)
        client.auth(self.api_key)
        return client

    def heropoints(self) -> "HeroPoints":
        client = HeroPoints(self.character_name)
        client.auth(self.api_key)
        return client

    def buildtabs(self) -> "BuildTabs":
        client = BuildTabs(self.character_name)
        client.auth(self.api_key)
        return client

    async def __aenter__(self) -> "Character":
        return self


class Backstory(
    _Character, Base[characters.CharacterBackstory], _type=characters.CharacterBackstory
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/backstory"


class Core(_Character, Base[characters.CharacterCore], _type=characters.CharacterCore):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/core"


class Crafting(
    _Character, Base[characters.CharacterCrafting], _type=characters.CharacterCrafting
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/crafting"


class Equipment(
    _Character, Base[characters.CharacterEquipment], _type=characters.CharacterEquipment
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/equipment"


class HeroPoints(_Character, ListBase[str], _type=str):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/heropoints"


class BuildTabs(_Character, Base[characters.BuildTab], _type=characters.BuildTab):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/buildtabs"
