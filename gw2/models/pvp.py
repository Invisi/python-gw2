import datetime
from typing import Literal

from pydantic import AnyHttpUrl, Field

from . import common
from ._base import BaseModel


class Amulet(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/amulets
    """

    id: int
    name: str
    icon: AnyHttpUrl
    attributes: dict[common.Attribute, int]


class WinLoss(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/stats
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/teams
    """

    wins: int
    losses: int
    desertions: int
    byes: int
    forfeits: int


class Ladders(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/stats
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/teams
    """

    unranked: WinLoss
    ranked: WinLoss
    two_vs_two_ranked: WinLoss | None = Field(alias="2v2ranked", default=None)
    three_vs_three_ranked: WinLoss | None = Field(alias="3v3ranked", default=None)
    solo_arena_rated: WinLoss | None = Field(alias="soloarenarated", default=None)
    team_arena_rated: WinLoss | None = Field(alias="teamarenarated", default=None)


class Game(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/stats
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/teams
    """

    class Score(BaseModel):
        red: int
        blue: int

    id: str
    map_id: int
    started: datetime.datetime
    ended: datetime.datetime
    result: Literal[
        "Victory", "Defeat", "Bye", "Forfeit"
    ]  # todo: probably some other results
    team: Literal["Red", "Blue"]
    profession: common.Profession
    scores: Score
    rating_type: Literal["Ranked", "Unranked", "None"]
    rating_change: int | None = None
    season: str | None = None


class Hero(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/heroes
    """

    class Skin(BaseModel):
        id: int
        name: str
        icon: AnyHttpUrl
        default: bool
        unlock_items: list[int] | None = None

    class Stats(BaseModel):
        offense: int
        defense: int
        speed: int

    id: str
    name: str
    description: str
    type: str
    stats: Stats
    overlay: AnyHttpUrl
    underlay: AnyHttpUrl
    skins: list[Skin]


class PvPRank(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/ranks
    """

    class Level(BaseModel):
        min_rank: int
        max_rank: int
        points: int

    id: int
    finisher_id: int
    name: str
    icon: AnyHttpUrl
    min_rank: int
    max_rank: int
    levels: list[Level]


class SeasonLeaderboard(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/seasons
    """

    class Ladder(BaseModel):
        class Settings(BaseModel):
            class Tier(BaseModel):
                range: tuple[int, int]

            name: str
            duration: int | None = None
            scoring: str
            tiers: list[Tier]

        class Scoring(BaseModel):
            id: str
            type: Literal["Integer"]
            description: str
            name: Literal["Rating", "Wins", "Losses"]
            ordering: Literal["MoreIsBetter", "LessIsBetter"]

        settings: Settings
        scorings: list[Scoring]

    ladder: Ladder


class OldSeasonLeaderboard(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/seasons
    """

    class OldLadder(BaseModel):
        class Settings(BaseModel):
            class Tier(BaseModel):
                range: tuple[int | float, int | float]
                color: str | None = None
                type: Literal["Rank"] | None = None
                name: (
                    Literal["Copper", "Bronze", "Silver", "Gold", "Platinum"] | None
                ) = None

            name: str
            duration: int | None = None
            scoring: str
            tiers: list[Tier]

        class Scoring(BaseModel):
            id: str
            type: Literal["Integer"]
            description: str
            name: Literal["Prestige", "Skill Rating", "Wins", "Losses"]
            ordering: Literal["MoreIsBetter", "LessIsBetter"]

        settings: Settings
        scorings: list[Scoring]

    legendary: OldLadder
    guild: OldLadder


class Season(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/seasons
    """

    class Division(BaseModel):
        class Tier(BaseModel):
            points: int

        name: str
        flags: list[Literal["CanLosePoints", "CanLoseTiers", "Repeatable"]]
        large_icon: AnyHttpUrl
        small_icon: AnyHttpUrl
        pip_icon: AnyHttpUrl
        tiers: list[Tier]

    class Rank(BaseModel):
        class Tier(BaseModel):
            rating: int

        name: str
        description: str
        icon: AnyHttpUrl
        overlay: AnyHttpUrl
        overlay_small: AnyHttpUrl
        tiers: list[Tier]

    id: str
    name: str
    start: datetime.datetime
    end: datetime.datetime
    active: bool
    divisions: list[Division]
    ranks: list[Rank] | None = None
    leaderboards: SeasonLeaderboard | OldSeasonLeaderboard


class LeaderboardLadder(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/seasons/:id/leaderboards
    """

    class Score(BaseModel):
        id: str
        value: int

    name: str
    rank: int
    date: datetime.datetime
    scores: list[Score]


class Standings(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/standings
    """

    class Best(BaseModel):
        total_points: int
        division: int
        tier: int
        points: int
        repeats: int

    class Current(Best):
        rating: int | None = None
        decay: int | None = None

    current: Current
    best: Best
    season_id: str


class Stats(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/stats
    """

    pvp_rank: int
    pvp_rank_points: int
    pvp_rank_rollovers: int
    aggregate: WinLoss
    professions: dict[
        Literal[
            "elementalist",
            "engineer",
            "guardian",
            "mesmer",
            "necromancer",
            "ranger",
            "revenant",
            "thief",
            "warrior",
        ],
        WinLoss,
    ]
    ladders: Ladders
