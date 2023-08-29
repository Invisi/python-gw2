import datetime
from typing import Literal

from .._base import BaseModel

Access = Literal[
    "PlayForFree",
    # Core game
    "GuildWars2",
    # Expansions
    "HeartOfThorns",
    "PathOfFire",
    "EndOfDragons",
]


class Account(BaseModel):
    id: str
    name: str
    age: int
    world: int
    guilds: list[str]
    created: datetime.datetime
    access: list[Access]
    commander: bool

    last_modified: datetime.datetime

    # guilds scope
    guild_leader: list[str] | None = None

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
