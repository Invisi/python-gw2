from typing import Literal

from ._base import BaseModel
from .common import ArmorType, Discipline, Weapon

Trinket = Literal[
    "Amulet",
    "Earring",
    "Ring",
]

Food = Literal[
    "Dessert",
    "Feast",
    "IngredientCooking",
    "Meal",
    "Seasoning",
    "Snack",
    "Soup",
    "Food",
]

CraftingComponent = Literal[
    "Component",
    "Inscription",
    "Insignia",
    "LegendaryComponent",
]


Refinement = Literal[
    "Refinement",
    "RefinementEctoplasm",
    "RefinementObsidian",
]


Guild = Literal[
    "GuildConsumable",
    "GuildDecoration",
    "GuildConsumableWvw",
]

Other = Literal[
    "Backpack",
    "Bag",
    "Bulk",
    "Consumable",
    "Dye",
    "Food",
    "Potion",
    "UpgradeComponent",
]

RecipeType = (
    Weapon | ArmorType | Trinket | Food | CraftingComponent | Refinement | Guild | Other
)


class Ingredient(BaseModel):
    item_id: int
    count: int
    # new type in schema 2022-03-09: "Currency"|"Item"


class GuildIngredient(BaseModel):
    upgrade_id: int
    count: int


class Recipe(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/recipes
    """

    # todo: upgrade for currency input, schema 2022-03-09

    id: int
    type: RecipeType
    output_item_id: int
    output_item_count: int
    time_to_craft_ms: int
    disciplines: list[Discipline]
    min_rating: int
    flags: list[Literal["AutoLearned", "LearnedFromItem"]]
    ingredients: list[Ingredient]
    guild_ingredients: list[GuildIngredient] | None = None
    output_upgrade_id: int | None = None
    chat_link: str
