import enum
from typing import List, Literal, Optional

from gw2.models._base import BaseModel


class Region(enum.Enum):
    TYRIA = "Tyria"
    MAGUUMA = "Maguuma"
    DESERT = "Desert"
    TUNDRA = "Tundra"


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

        id: Optional[int]
        count: Optional[int]
        region: Optional[Region]

    class Bit(BaseModel):
        type: Literal["Text", "Item", "Minipet", "Skin"]
        id: Optional[int]
        text: Optional[str]

    id: int
    icon: Optional[str] = None
    name: str
    description: str
    requirement: str
    locked_text: str
    type: Literal["Default", "ItemSet"]

    flags: List[Flag] = []
    tiers: List[Tier] = []
    rewards: Optional[List[Reward]]
    bits: Optional[List[Bit]]

    point_cap: Optional[int]
