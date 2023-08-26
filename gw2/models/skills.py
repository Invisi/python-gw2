import enum

from pydantic import AnyHttpUrl, validator

from ._base import BaseModel
from .common import Fact, Profession, SkillSlot, TraitedFact, Weapon, coerce_weapon


class Type(enum.Enum):
    BUNDLE = "Bundle"
    ELITE = "Elite"
    HEAL = "Heal"
    MONSTER = "Monster"
    PET = "Pet"
    PROFESSION = "Profession"
    TOOLBELT = "Toolbelt"
    TRANSFORM = "Transform"
    UTILITY = "Utility"
    WEAPON = "Weapon"


class Attunement(enum.Enum):
    FIRE = "Fire"
    WATER = "Water"
    AIR = "Air"
    EARTH = "Earth"


class Skill(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/skills
    """

    id: int
    name: str
    description: str
    icon: AnyHttpUrl | None = None
    chat_link: str
    type: Type | None = None
    weapon_type: Weapon | None = None
    professions: list[Profession] | None = None
    slot: SkillSlot | None = None
    fact: list[Fact] | None = None
    traited_facts: list[TraitedFact] | None = None
    categories: list[str] | None = None  # todo: types
    attunement: Attunement | None = None
    cost: int | None = None
    dual_wield: str | None
    flip_skill: int | None = None
    initiative: int | None = None
    next_chain: int | None = None
    prev_chain: int | None = None
    transform_skills: list[int] | None = None
    bundle_skills: list[int] | None = None
    toolbelt_skill: int | None = None
    flags: list[str] | None = None  # todo: types

    _normalize_type = validator("weapon_type", pre=True, allow_reuse=True)(
        coerce_weapon
    )
