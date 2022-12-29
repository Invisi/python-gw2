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
    guilds: list[uuid.UUID]
    created: datetime.datetime
    access: list[Access]
    commander: bool

    last_modified: datetime.datetime

    # guilds scope
    guild_leader: list[uuid.UUID] | None = None

    # progression scope
    fractal_level: int | None = None
    daily_ap: int | None = None
    monthly_ap: int | None = None
    wvw_rank: int | None = None

    build_storage_slots: int | None = None


class Achievement(BaseModel):
    id: int
    done: bool

    # Optional
    bits: list[int] | None = None
    current: int | None = None
    max: int | None = None
    repeated: int | None = None
    unlocked: bool | None = None
