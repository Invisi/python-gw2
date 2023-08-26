import enum

from pydantic import AnyHttpUrl, validator

from ._base import BaseModel
from .common import ArmorType, ArmorWeight, Weapon, coerce_weapon


class Type(enum.Enum):
    ARMOR = "Armor"
    WEAPON = "Weapon"
    BACK = "Back"
    GATHERING = "Gathering"


class Flag(enum.Enum):
    SHOW_IN_WARDROBE = "ShowInWardrobe"
    NO_COST = "NoCost"
    HIDE_IF_LOCKED = "HideIfLocked"
    OVERRIDE_RARITY = "OverrideRarity"


class DyeMaterial(enum.Enum):
    CLOTH = "cloth"
    LEATHER = "leather"
    METAL = "metal"


class DyeSlot(BaseModel):
    color_id: int
    material: DyeMaterial


class DyeSlotOverrides(BaseModel):
    AsuraMale: list[DyeSlot | None] | None = None
    AsuraFemale: list[DyeSlot | None] | None = None
    CharrMale: list[DyeSlot | None] | None = None
    CharrFemale: list[DyeSlot | None] | None = None
    HumanMale: list[DyeSlot | None] | None = None
    HumanFemale: list[DyeSlot | None] | None = None
    NornMale: list[DyeSlot | None] | None = None
    NornFemale: list[DyeSlot | None] | None = None
    SylvariMale: list[DyeSlot | None] | None = None
    SylvariFemale: list[DyeSlot | None] | None = None


class DyeSlots(BaseModel):
    default: list[DyeSlot | None]
    overrides: DyeSlotOverrides


class WeaponDamage(enum.Enum):
    PHYSICAL = "Physical"
    FIRE = "Fire"
    LIGHTNING = "Lightning"
    ICE = "Ice"
    CHOKING = "Choking"


class GatheringType(enum.Enum):
    FORAGING = "Foraging"
    LOGGING = "Logging"
    MINING = "Mining"
    LURE = "Lure"  # todo: add to wiki
    BAIT = "Bait"  # todo: add to wiki
    FISHING = "Fishing"  # todo: add to wiki


class Details(BaseModel):
    type: Weapon | ArmorType | GatheringType
    damage_type: WeaponDamage | None = None
    weight_class: ArmorWeight | None = None
    dye_slots: DyeSlots | None = None

    _normalize_type = validator("type", pre=True, allow_reuse=True)(coerce_weapon)


class Skin(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/skills
    """

    id: int
    name: str
    type: Type
    flags: list[Flag]
    restrictions: list[str]  # todo: types
    icon: AnyHttpUrl | None = None
    rarity: str  # todo: types
    description: str | None = None
    details: Details | None = None
