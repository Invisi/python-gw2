from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import Fact, TraitedFact


class Skill(BaseModel):
    id: int
    name: str
    description: str
    icon: AnyHttpUrl | None = None
    facts: list[Fact] | None = None
    traited_facts: list[TraitedFact] | None = None
    flags: list[int]
    chat_link: str
    categories: list[
        Literal[
            "Arcane",
            "Burst",
            "Cantrip",
            "Clone",
            "Corruption",
            "Elixir",
            "Gadget",
            "Glamour",
            "LegendaryDwarf",
            "Mark",
            "Meditation",
            "Overload",
            "Phantasm",
            "Physical",
            "PrimalBurst",
            "Rage",
            "Shout",
            "Signet",
            "Stance",
            "Survival",
            "Symbol",
            "Trick",
            "Venom",
            "Virtue",
        ]
    ] | None = None


class Trait(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/traits
    """

    id: int
    name: str
    icon: AnyHttpUrl
    description: str | None = None
    specialization: int
    tier: int
    slot: Literal["Minor", "Major"]
    facts: list[Fact] | None = None
    traited_facts: list[TraitedFact] | None = None
    skills: list[Skill] | None = None
    order: int
