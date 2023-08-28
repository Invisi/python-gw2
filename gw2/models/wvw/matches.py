import datetime
from typing import Literal

from .._base import BaseModel

Colors = Literal["red", "green", "blue"]
MapType = Literal[
    "RedHome",
    "GreenHome",
    "BlueHome",
    "Center",
]
ObjectiveType = Literal[
    "Camp",
    "Keep",
    "Mercenary",
    "Ruins",
    "Spawn",
    "Tower",
    "Castle",
]


class Bonus(BaseModel):
    type: Literal["Bloodlust"]
    owner: Literal["Red", "Green", "Blue"]


class Objective(BaseModel):
    id: str
    type: ObjectiveType
    owner: Literal["Red", "Green", "Blue", "Neutral"]
    last_flipped: datetime.datetime
    claimed_by: str | None = None
    claimed_at: datetime.datetime | None = None
    points_tick: int
    points_capture: int
    guild_upgrades: list[int] | None = None
    yaks_delivered: int | None = None


class Map(BaseModel):
    id: int
    type: MapType
    scores: dict[Colors, int]
    bonuses: list[Bonus]
    deaths: dict[Colors, int]
    kills: dict[Colors, int]
    objectives: list[Objective]


class MapScore(BaseModel):
    type: MapType
    scores: dict[Colors, int]


class Skirmish(BaseModel):
    id: int
    scores: dict[Colors, int]
    map_scores: list[MapScore]


class Match(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/matches
    """

    id: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    scores: dict[Colors, int]
    worlds: dict[Colors, int]
    all_worlds: dict[Colors, list[int]]
    deaths: dict[Colors, int]
    kills: dict[Colors, int]
    maps: list[Map]
    skirmishes: list[Skirmish]
    victory_points: dict[Colors, int]


class MatchOverview(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/matches
    """

    id: str
    worlds: dict[Colors, int]
    all_worlds: dict[Colors, list[int]]
    start_time: datetime.datetime
    end_time: datetime.datetime
