from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field, field_validator

from ..utils import EnumValidator
from ._base import BaseModel, Unknown
from .common import Attunement, SkillSlot, Weapon
from .common import Profession as GameProfession


class SkillTrack(BaseModel):
    cost: int
    type: Literal["Skill"]
    skill_id: int


class TraitTrack(BaseModel):
    cost: int
    type: Literal["Trait"]
    trait_id: int


class Training(BaseModel):
    id: int
    category: Literal[
        "Skills",
        "Specializations",
        "EliteSpecializations",
    ]
    name: str
    track: list[Annotated[SkillTrack | TraitTrack, Field(discriminator="type")]]


class WeaponSkill(BaseModel):
    id: int
    slot: SkillSlot
    offhand: Weapon | Literal["Nothing"] | None = None
    attunement: Attunement | None = None
    source: GameProfession | None = None


class WeaponDetails(BaseModel):
    flags: list[Literal["Mainhand", "Offhand", "TwoHand", "Aquatic"]]
    specialization: int | None = None
    skills: list[WeaponSkill]


class Skill(BaseModel):
    id: int
    slot: SkillSlot
    type: Literal[
        "Elite",
        "Heal",
        "Profession",
        "Utility",
    ]
    source: GameProfession | None = None
    attunement: Attunement | None = None


class Profession(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/professions
    """

    id: str
    name: GameProfession
    code: int  # profession code for build template links
    icon: AnyHttpUrl
    icon_big: AnyHttpUrl
    specializations: list[int]
    skills: list[Skill]
    training: list[Training]
    weapons: dict[Weapon, WeaponDetails]
    flags: list[
        Annotated[
            Literal["NoRacialSkills", "NoWeaponSwap"],
            EnumValidator,
        ]
        | Unknown
    ]
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
