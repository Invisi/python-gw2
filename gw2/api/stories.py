import functools

from gw2 import models

from ._base import Base, IdsBase


class Stories(IdsBase[models.Story, int]):
    pass


class Story(Base[models.Story]):
    def __init__(self, story_id: int):
        self.story_id = story_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/{self.story_id}"


class StorySeasons(IdsBase[models.StorySeason, str]):
    suffix = "stories/seasons"


class StorySeason(Base[models.StorySeason]):
    def __init__(self, quest_id: str):
        self.quest_id = quest_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/seasons/{self.quest_id}"
