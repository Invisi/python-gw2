import datetime
from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel

Colors = Literal["red", "green", "blue"]
MapType = Literal["RedHome", "GreenHome", "BlueHome", "Center", "EdgeOfTheMists"]
ObjectiveType = Literal[
    "Camp",
    "Keep",
    "Mercenary",
    "Ruins",
    "Spawn",
    "Tower",
    "Castle",
    "Generic",
    "Resource",
]


class Bonus(BaseModel):
    type: Literal["Bloodlust"]
    owner: Literal["Red", "Green", "Blue"]


class _Objective(BaseModel):
    id: str
    type: ObjectiveType

    guild_upgrades: list[int] | None = None
    yaks_delivered: int | None = None


class Objective(_Objective):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/objectives
    """

    name: str
    sector_id: int
    map_id: int
    map_type: MapType
    coord: tuple[float, float, float] | None = None
    label_coord: tuple[float, float] | None = None
    marker: AnyHttpUrl | None = None
    chat_link: str
    upgrade_id: int | None = None


class MapObjective(_Objective):
    owner: Literal["Red", "Green", "Blue", "Neutral"]
    last_flipped: datetime.datetime
    claimed_by: str | None = None
    claimed_at: datetime.datetime | None = None
    points_tick: int
    points_capture: int


class Map(BaseModel):
    id: int
    type: MapType
    scores: dict[Colors, int]
    bonuses: list[Bonus]
    deaths: dict[Colors, int]
    kills: dict[Colors, int]
    objectives: list[MapObjective]


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


class MatchScore(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/matches
    """

    class _MapScore(MapScore):
        id: int

    id: str
    scores: dict[Colors, int]
    maps: list[_MapScore]
    skirmishes: list[Skirmish]
    victory_points: dict[Colors, int]


class MatchStat(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/matches
    """

    class Map(BaseModel):
        id: int
        type: MapType
        deaths: dict[Colors, int]
        kills: dict[Colors, int]

    id: str
    deaths: dict[Colors, int]
    kills: dict[Colors, int]
    maps: list[Map]


class WvWRank(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/ranks
    """

    id: int
    title: str
    min_rank: int


class WvWUpgrade(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/wvw/upgrades
    """

    class Tier(BaseModel):
        class Upgrade(BaseModel):
            name: str
            description: str
            icon: AnyHttpUrl

        name: Literal["Secured", "Reinforced", "Fortified"]
        yaks_required: int
        upgrades: list[Upgrade]

    id: int
    tiers: list[Tier]
