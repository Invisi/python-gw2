import functools

from gw2 import models

from ._base import Base, IdsBase

# todo: match based on world_id


class Matches(IdsBase[models.Match, str]):
    suffix = "wvw/matches"


class Match(Base[models.Match]):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/{self.match_id}"


class MatchOverviews(IdsBase[models.MatchOverview, str]):
    suffix = "wvw/matches/overview"


class MatchOverview(Base[models.MatchOverview]):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/overview/{self.match_id}"


class MatchScores(IdsBase[models.MatchScore, str]):
    suffix = "wvw/matches/scores"


class MatchScore(Base[models.MatchScore]):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/scores/{self.match_id}"


class MatchStats(IdsBase[models.MatchStat, str]):
    suffix = "wvw/matches/stats"


class MatchStat(Base[models.MatchStat]):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/stats/{self.match_id}"


class Objectives(IdsBase[models.Objective, str]):
    suffix = "wvw/objectives"


class Objective(Base[models.Objective]):
    def __init__(self, objective_id: str):
        self.objective_id = objective_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/objectives/{self.objective_id}"


class WvWRanks(IdsBase[models.WvWRank, int]):
    suffix = "wvw/ranks"


class WvWRank(Base[models.WvWRank]):
    def __init__(self, rank_id: int):
        self.rank_id = rank_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/ranks/{self.rank_id}"


class WvWUpgrades(IdsBase[models.WvWUpgrade, int]):
    suffix = "wvw/upgrades"


class WvWUpgrade(Base[models.WvWUpgrade]):
    def __init__(self, upgrade_id: int):
        self.upgrade_id = upgrade_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/upgrades/{self.upgrade_id}"
