import enum
from typing import Literal

from .._base import BaseModel

Region = Literal["Tyria", "Maguuma", "Desert", "Tundra", "Unknown", "Cantha"]


class Tier(BaseModel):
    count: int
    points: int


class Reward(BaseModel):
    type: Literal["Coins", "Item", "Mastery", "Title"]  # todo: tagged union

    id: int | None = None
    count: int | None = None
    # XXX: Cantha is currently reported as Unknown
    region: Region | None = None


class Bit(BaseModel):
    type: Literal["Text", "Item", "Minipet", "Skin"] | None = None  # todo: tagged union
    id: int | None = None
    text: str | None = None


class Achievement(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements
    """

    id: int
    icon: str | None = None
    name: str
    description: str
    requirement: str
    locked_text: str
    type: Literal["Default", "ItemSet"]

    flags: list[
        Literal[
            "Pvp",
            "CategoryDisplay",
            "MoveToTop",
            "IgnoreNearlyComplete",
            "Repeatable",
            "Hidden",
            "RequiresUnlock",
            "RepairOnLogin",
            "Daily",
            "Weekly",
            "Monthly",
            "Permanent",
        ]
    ] | None = None
    tiers: list[Tier] | None = None
    rewards: list[Reward] | None = None
    bits: list[Bit] | None = None

    point_cap: int | None = None
    prerequisites: list[int] | None = None
