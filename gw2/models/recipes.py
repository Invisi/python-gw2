import enum

from ._base import BaseModel
from .common import ArmorType, Discipline, Weapon


class TypeTrinket(enum.Enum):
    AMULET = "Amulet"
    EARRING = "Earring"
    RING = "Ring"


class TypeFood(enum.Enum):
    DESSERT = "Dessert"
    FEAST = "Feast"
    INGREDIENT_COOKING = "IngredientCooking"
    MEAL = "Meal"
    SEASONING = "Seasoning"
    SNACK = "Snack"
    SOUP = "Soup"
    FOOD = "Food"


class TypeCraftingComponent(enum.Enum):
    COMPONENT = "Component"
    INSCRIPTION = "Inscription"
    INSIGNIA = "Insignia"
    LEGENDARY_COMPONENT = "LegendaryComponent"


class TypeRefinement(enum.Enum):
    REFINEMENT = "Refinement"
    REFINEMENT_ECTOPLASM = "RefinementEctoplasm"
    REFINEMENT_OBSIDIAN = "RefinementObsidian"


class TypeGuild(enum.Enum):
    GUILD_CONSUMABLE = "GuildConsumable"
    GUILD_DECORATION = "GuildDecoration"
    GUILD_CONSUMABLE_WVW = "GuildConsumableWvw"


class TypeOther(enum.Enum):
    BACKPACK = "Backpack"
    BAG = "Bag"
    BULK = "Bulk"
    CONSUMABLE = "Consumable"
    DYE = "Dye"
    FOOD = "Food"
    POTION = "Potion"
    UPGRADE_COMPONENT = "UpgradeComponent"


class Flag(enum.Enum):
    AUTO_LEARNED = "AutoLearned"
    LEARNED_FROM_ITEM = "LearnedFromItem"


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
    type: (
        Weapon
        | ArmorType
        | TypeTrinket
        | TypeFood
        | TypeCraftingComponent
        | TypeRefinement
        | TypeGuild
        | TypeOther
    )
    output_item_id: int
    output_item_count: int
    time_to_craft_ms: int
    disciplines: list[Discipline]
    min_rating: int
    flags: list[Flag]
    ingredients: list[Ingredient]
    guild_ingredients: list[GuildIngredient] | None = None
    output_upgrade_id: int | None = None
    chat_link: str
