import datetime
from typing import Literal

from . import common
from ._base import BaseModel


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


class Game(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pvp/stats
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/teams
    """

    id: str
    map_id: int
    started: datetime.datetime
    ended: datetime.datetime
    result: Literal["Victory", "Defeat"]
    profession: common.Profession
    scores: dict[Literal["red", "blue"], int]
    rating_type: Literal["Ranked", "Unranked", None]
    rating_change: int
    season: str | None = None
