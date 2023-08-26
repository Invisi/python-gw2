import enum
from typing import Literal

from .._base import BaseModel

Region = Literal["Tyria", "Maguuma", "Desert", "Tundra", "Unknown", "Cantha"]


class Achievement(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements
    """

    class Flag(enum.Enum):
        PVP = "Pvp"
        CATEGORY_DISPLAY = "CategoryDisplay"
        MOVE_TO_TOP = "MoveToTop"
        IGNORE_NEARLY_COMPLETE = "IgnoreNearlyComplete"
        REPEATABLE = "Repeatable"
        HIDDEN = "Hidden"
        REQUIRES_UNLOCK = "RequiresUnlock"
        REPAIR_ON_LOGIN = "RepairOnLogin"
        DAILY = "Daily"
        WEEKLY = "Weekly"
        MONTHLY = "Monthly"
        PERMANENT = "Permanent"

    class Tier(BaseModel):
        count: int
        points: int

    class Reward(BaseModel):
        # TODO: Extended validation based on type?
        type: Literal["Coins", "Item", "Mastery", "Title"]

        id: int | None
        count: int | None
        # XXX: Cantha is currently reported as Unknown
        region: Region | None

    class Bit(BaseModel):
        type: Literal["Text", "Item", "Minipet", "Skin"] | None
        id: int | None
        text: str | None

    id: int
    icon: str | None = None
    name: str
    description: str
    requirement: str
    locked_text: str
    type: Literal["Default", "ItemSet"]

    flags: list[Flag] = []
    tiers: list[Tier] = []
    rewards: list[Reward] | None
    bits: list[Bit] | None

    point_cap: int | None
