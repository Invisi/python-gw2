import functools
from typing import Literal

from gw2 import models

from ._base import AllIdsBase, Base, IdsBase, ListBase


class Amulets(IdsBase[models.Amulet, int]):
    suffix = "pvp/amulets"


class Amulet(Base[models.Amulet]):
    def __init__(self, amulet_id: int):
        self.amulet_id = amulet_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/amulets/{self.amulet_id}"


class Games(IdsBase[models.Game, str]):
    suffix = "pvp/games"


class Game(Base[models.Game]):
    def __init__(self, game_id: str):
        self.game_id = game_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/games/{self.game_id}"


class Heroes(IdsBase[models.Hero, str]):
    suffix = "pvp/heroes"


class Hero(Base[models.Hero]):
    def __init__(self, hero_id: str):
        self.hero_id = hero_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/heroes/{self.hero_id}"


class PvPRanks(IdsBase[models.PvPRank, int]):
    suffix = "pvp/ranks"


class PvPRank(Base[models.PvPRank]):
    def __init__(self, rank_id: int):
        self.rank_id = rank_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/ranks/{self.rank_id}"


class Seasons(AllIdsBase[models.Season, int]):
    suffix = "pvp/seasons"


class Season(Base[models.Season]):
    def __init__(self, season_id: str):
        self.season_id = season_id
        super().__init__()

    def leaderboards(self, region: Literal["na", "eu"]) -> "Leaderboards":
        client = Leaderboards(self.season_id, region)
        return client

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/seasons/{self.season_id}"


class Leaderboards(ListBase[models.LeaderboardLadder]):
    def __init__(self, season_id: str, region: Literal["na", "eu"]):
        self.season_id = season_id
        self.region = region
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"pvp/seasons/{self.season_id}/leaderboards/ladder/{self.region}"


class Standings(ListBase[models.Standings]):
    suffix = "pvp/standings"


class Stats(Base[models.Stats]):
    suffix = "pvp/stats"
