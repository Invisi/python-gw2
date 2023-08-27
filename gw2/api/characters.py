import functools

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

    def hero_points(self) -> "HeroPoints":
        client = HeroPoints(self.character_name)
        client.auth(self.api_key)
        return client

    def build_tabs(self) -> "BuildTabs":
        client = BuildTabs(self.character_name)
        client.auth(self.api_key)
        return client

    async def __aenter__(self) -> "Character":
        return self


class Backstory(_Character, Base[characters.Backstory], _type=characters.Backstory):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/backstory"


class Core(_Character, Base[characters.Core], _type=characters.Core):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/core"


class Crafting(_Character, Base[characters.Crafting], _type=characters.Crafting):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/crafting"


class Equipment(_Character, Base[characters.Equipment], _type=characters.Equipment):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/equipment"


class HeroPoints(_Character, ListBase[str], _type=str):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/heropoints"


class BuildTabs(
    _Character,
    IdsBase[characters.BuildTab, int],
    _type=characters.BuildTab,
    _ids_param="tabs",
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/buildtabs"
