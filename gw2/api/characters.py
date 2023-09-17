import functools

from gw2 import models
from gw2.models import characters

from ._base import Base, IdsBase, ListBase


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

    def build_tabs(self) -> "BuildTabs":
        client = BuildTabs(self.character_name)
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

    def equipment_tabs(self) -> "EquipmentTabs":
        client = EquipmentTabs(self.character_name)
        client.auth(self.api_key)
        return client

    def inventory(self) -> "Inventory":
        client = Inventory(self.character_name)
        client.auth(self.api_key)
        return client

    def quests(self) -> "Quests":
        client = Quests(self.character_name)
        client.auth(self.api_key)
        return client

    def recipes(self) -> "Recipes":
        client = Recipes(self.character_name)
        client.auth(self.api_key)
        return client

    def sab(self) -> "SuperAdventureBox":
        client = SuperAdventureBox(self.character_name)
        client.auth(self.api_key)
        return client

    async def __aenter__(self) -> "Character":
        return self


class Backstory(_Character, Base[characters.Backstory], _type=characters.Backstory):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/backstory"


class BuildTabs(
    _Character,
    IdsBase[characters.BuildTab, int],
    _type=characters.BuildTab,
    _ids_param="tabs",
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/buildtabs"


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


class EquipmentTabs(
    _Character,
    IdsBase[characters.EquipmentTabs, int],
    _type=characters.EquipmentTabs,
    _ids_param="tabs",
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/equipmenttabs"


class Inventory(_Character, Base[characters.Inventory], _type=characters.Inventory):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/inventory"


class Quests(_Character, ListBase[int], _type=int):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/quests"


class Recipes(_Character, Base[characters.Recipes], _type=characters.Recipes):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/recipes"


class SuperAdventureBox(
    _Character, Base[characters.SuperAdventureBox], _type=characters.SuperAdventureBox
):
    @functools.cached_property
    def suffix(self) -> str:
        return f"characters/{self.character_name}/sab"
