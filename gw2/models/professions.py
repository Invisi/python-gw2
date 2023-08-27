import enum
from typing import Literal

from pydantic import AnyHttpUrl, field_validator

from ._base import BaseModel
from .common import SkillSlot, Weapon


class TrainingCategory(enum.Enum):
    SKILLS = "Skills"
    SPECIALIZATIONS = "Specializations"
    ELITE_SPECIALIZATIONS = "EliteSpecializations"


class TrainingTrack(BaseModel):
    cost: int
    type: Literal["Trait", "Skill"]
    skill_id: int | None = None
    trait_id: int | None = None


class Training(BaseModel):
    id: int
    category: TrainingCategory
    name: str
    track: list[TrainingTrack]


class Skill(BaseModel):
    id: int
    slot: SkillSlot
    offhand: str | None = None
    attunement: str | None = None
    source: str | None = None


class WeaponDetails(BaseModel):
    flags: list[Literal["Mainhand", "Offhand", "TwoHand", "Aquatic"]]
    specialization: int | None = None
    skills: list[Skill]


class Flag(enum.Enum):
    NO_RACIAL_SKILLS = "NoRacialSkills"
    NO_WEAPON_SWAP = "NoWeaponSwap"


class Profession(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/professions
    """

    id: str
    name: str
    code: int  # profession code for build template links
    icon: AnyHttpUrl
    icon_big: AnyHttpUrl
    specializations: list[int]
    training: list[Training]
    weapons: dict[Weapon, WeaponDetails]
    flags: list[Flag]
    skills_by_palette: list[tuple[int, int]]  # [(skill palette id, skill id)]

    @field_validator("weapons", mode="before")
    def normalize_weapon_type(
        cls,  # noqa: N805
        val: dict[str, dict],
    ) -> dict[str, dict]:
        if "Shortbow" in val:
            val["ShortBow"] = val["Shortbow"]
            del val["Shortbow"]

        if "Longbow" in val:
            val["LongBow"] = val["Longbow"]
            del val["Longbow"]

        if "Spear" in val:
            val["Harpoon"] = val["Spear"]
            del val["Spear"]

        return val
