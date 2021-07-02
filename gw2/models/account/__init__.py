import dataclasses

# TODO: Ignore unexpected keywords via custom global __init__
import datetime
import enum
import uuid
from typing import List, Optional

from gw2.models._base import BaseModel


class Access(enum.Enum):
    PLAY_FOR_FREE = "PlayForFree"
    # Core game
    GUILD_WARS2 = "GuildWars2"
    # Expansions
    HEART_OF_THORNS = "HeartOfThorns"
    PATH_OF_FIRE = "PathOfFire"
    END_OF_DRAGONS = "EndOfDragons"


class Account(BaseModel):
    id: uuid.UUID
    name: str
    age: int
    world: int
    guilds: List[uuid.UUID]
    created: datetime.datetime
    access: List[Access]
    commander: bool

    last_modified: datetime.datetime

    # guilds scope
    guild_leader: Optional[List[str]] = None

    # progression scope
    fractal_level: Optional[int] = None
    daily_ap: Optional[int] = None
    monthly_ap: Optional[int] = None
    wvw_rank: Optional[int] = None

    build_storage_slots: Optional[int] = None


class Achievement(BaseModel):
    id: int
    done: bool

    # Optional
    bits: Optional[List[int]] = None
    current: Optional[int] = None
    max: Optional[int] = None
    repeated: Optional[int] = None
    unlocked: Optional[bool] = None
