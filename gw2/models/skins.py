from typing import Literal

from pydantic import AnyHttpUrl, field_validator

from ._base import BaseModel
from .common import (
    ArmorType,
    ArmorWeight,
    DyeSlot,
    Rarity,
    Weapon,
    WeaponDamage,
    coerce_weapon,
)


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


# todo: last three are missing on wiki
GatheringType = Literal["Foraging", "Logging", "Mining", "Lure", "Bait", "Fishing"]


class Details(BaseModel):
    type: Weapon | ArmorType | GatheringType  # todo: tagged union
    damage_type: WeaponDamage | None = None
    weight_class: ArmorWeight | None = None
    dye_slots: DyeSlots | None = None

    _normalize_type = field_validator("type", mode="before")(coerce_weapon)


class Skin(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/skills
    """

    id: int
    name: str
    type: Literal[
        "Armor",
        "Weapon",
        "Back",
        "Gathering",
    ]  # todo: tagged union
    flags: list[
        Literal[
            "ShowInWardrobe",
            "NoCost",
            "HideIfLocked",
            "OverrideRarity",
        ]
    ]
    restrictions: list[str]  # todo: types
    icon: AnyHttpUrl | None = None
    rarity: Rarity
    description: str | None = None
    details: Details | None = None
