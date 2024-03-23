from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import Region


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
    icon: AnyHttpUrl | None = None
    name: str
    description: str
    requirement: str
    locked_text: str
    type: Literal["Default", "ItemSet"]

    flags: (
        list[
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
        ]
        | None
    ) = None
    tiers: list[Tier] | None = None
    rewards: list[Reward] | None = None
    bits: list[Bit] | None = None

    point_cap: int | None = None
    prerequisites: list[int] | None = None


class AchievementCategory(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements/categories
    """

    # todo: upgrade schema to 2022-03-23 for extended data

    id: int
    name: str
    description: str
    order: int
    icon: AnyHttpUrl
    achievements: list[int]


class AchievementGroup(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements/groups
    """

    id: str
    name: str
    description: str
    order: int
    categories: list[int]
