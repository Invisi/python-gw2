import functools

from gw2 import models

from .._base import Base, IdsBase


class Matches(IdsBase[models.Match, str], _type=models.Match):
    suffix = "wvw/matches"


class Match(Base[models.Match], _type=models.Match):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/{self.match_id}"


class MatchOverviews(IdsBase[models.MatchOverview, str], _type=models.MatchOverview):
    suffix = "wvw/matches/overview"


class MatchOverview(Base[models.MatchOverview], _type=models.MatchOverview):
    def __init__(self, match_id: str):
        self.match_id = match_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wvw/matches/overview/{self.match_id}"
