import datetime
import uuid
from typing import Literal

from pydantic import Field

from ._base import BaseModel
from .common import Discipline, Gender, Profession, Race

EquipmentSlot = Literal[
    "Accessory1",
    "Accessory2",
    "Amulet",
    "Axe",
    "Backpack",
    "Boots",
    "Coat",
    "Gloves",
    "Helm",
    "HelmAquatic",
    "Leggings",
    "Pick",
    "Ring1",
    "Ring2",
    "Shoulders",
    "Sickle",
    "WeaponA1",
    "WeaponA2",
    "WeaponAquaticA",
    "WeaponAquaticB",
    "WeaponB1",
    "WeaponB2",
]
Binding = Literal["Account", "Character"]


Location = Literal[
    "Equipped",
    "Armory",
    "EquippedFromLegendaryArmory",
    "LegendaryArmory",
]

# --- Enums above, scary things below


class CraftingDetails(BaseModel):
    discipline: Discipline
    rating: int
    active: bool


class WvWAbility(BaseModel):
    id: int
    rank: int


class BuildTab(BaseModel):
    class Build(BaseModel):
        class Skills(BaseModel):
            heal: int | None
            utilities: list[int | None] = Field(min_length=3, max_length=3)
            elite: int | None

        class Specialization(BaseModel):
            id: int | None
            traits: list[int | None] = Field(min_length=3, max_length=3)

        name: str
        profession: Profession
        specializations: list[Specialization] = Field(min_length=3, max_length=3)
        skills: Skills
        aquatic_skills: Skills

        # TODO: Actual specialization since that's not in profession (spec ids)

    tab: int  # Tab number
    is_active: bool
    build: Build


class Stats(BaseModel):
    id: int
    # That's way too annoying to define in a clear way
    attributes: dict[str, int]


class EquipmentDetails(BaseModel):
    id: int
    slot: EquipmentSlot | None = None

    infusions: list[int] | None = None
    upgrades: list[int] | None = None
    skin: int | None = None
    stats: Stats | None = None
    binding: Binding | None = None
    location: Location
    tabs: list[int] | None = None
    charges: int | None = None
    bound_to: str | None = None
    dyes: list[int | None] | None = None


class EquipmentPvP(BaseModel):
    amulet: int | None
    rune: int | None
    sigils: list[int | None] = Field(min_length=4, max_length=4)


class EquipmentTabs(BaseModel):
    tab: int
    name: str
    is_active: bool
    equipment: list[EquipmentDetails]
    equipment_pvp: EquipmentPvP


class Training(BaseModel):
    id: int
    spent: int
    done: bool


class InventorySlot(BaseModel):
    id: int
    count: int
    charges: int | None = None
    infusions: list[int] | None = None
    upgrades: list[int] | None = None
    skin: int | None = None
    stats: Stats | None = None
    binding: Binding | None = None
    bound_to: str | None = None
    upgrade_slot_indices: list[int] | None = None
    dyes: list[int] | None = None


class Bag(BaseModel):
    id: int
    size: int
    inventory: list[InventorySlot | None]


class Character(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/characters
    """

    name: str
    race: Race
    gender: Gender
    flags: list[str]
    profession: Profession
    level: int
    guild: uuid.UUID | None = None
    age: int

    deaths: int
    crafting: list[CraftingDetails]
    title: int | None = None
    backstory: list[str]

    last_modified: datetime.datetime
    created: datetime.datetime

    wvw_abilities: list[WvWAbility]
    build_tabs_unlocked: int
    active_build_tab: int
    build_tabs: list[BuildTab]

    active_equipment_tab: int
    equipment: list[EquipmentDetails]
    equipment_tabs: list[EquipmentTabs]
    equipment_tabs_unlocked: int

    recipes: list[int]

    training: list[Training]
    bags: list[Bag | None]

    # TODO: Simplified access to inventory


# -- separate endpoints
class Backstory(BaseModel):
    backstory: list[str]


class Core(BaseModel):
    name: str
    race: Race
    gender: Gender
    profession: Profession
    level: int
    guild: uuid.UUID | None = None
    age: int
    deaths: int
    title: int | None = None

    created: datetime.datetime
    last_modified: datetime.datetime


class Crafting(BaseModel):
    crafting: list[CraftingDetails]


class Equipment(BaseModel):
    equipment: list[EquipmentDetails]
