import functools

from gw2 import models

from .._base import Base, IdsBase


class StorySeasons(IdsBase[models.StorySeason, str], _type=models.StorySeason):
    suffix = "stories/seasons"


class StorySeason(Base[models.StorySeason], _type=models.StorySeason):
    def __init__(self, quest_id: str):
        self.quest_id = quest_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/seasons/{self.quest_id}"
