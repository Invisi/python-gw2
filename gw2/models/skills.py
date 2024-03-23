from typing import Literal

from pydantic import AnyHttpUrl, field_validator

from ._base import BaseModel
from .common import (
    Attunement,
    Fact,
    Profession,
    SkillSlot,
    TraitedFact,
    Weapon,
    coerce_weapon,
)


class SubSkill(BaseModel):
    id: int
    attunement: Attunement | None = None
    form: Literal["CelestialAvatar"] | None = None


class Skill(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/skills
    """

    id: int
    attunement: Attunement | None = None
    bundle_skills: list[int] | None = None
    categories: list[str] | None = None  # todo: types
    chat_link: str
    cost: int | None = None
    description: str
    dual_wield: str | None = None
    dual_attunement: Attunement | None = None
    facts: list[Fact] | None = None
    flags: list[str] | None = None  # todo: types
    flip_skill: int | None = None
    icon: AnyHttpUrl | None = None
    initiative: int | None = None
    name: str
    next_chain: int | None = None
    prev_chain: int | None = None
    professions: list[Profession] | None = None
    slot: SkillSlot | None = None
    specialization: int | None = None
    subskills: list[SubSkill] | None = None
    toolbelt_skill: int | None = None
    traited_facts: list[TraitedFact] | None = None
    transform_skills: list[int] | None = None
    type: (
        Literal[
            "Bundle",
            "Elite",
            "Heal",
            "Monster",
            "Pet",
            "Profession",
            "Toolbelt",
            "Transform",
            "Utility",
            "Weapon",
        ]
        | None
    ) = None
    weapon_type: Weapon | None = None

    _normalize_type = field_validator("weapon_type", mode="before")(coerce_weapon)
