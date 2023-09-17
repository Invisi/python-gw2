import functools

from gw2 import models

from ._base import Base, IdsBase


class Stories(IdsBase[models.Story, int], _type=models.Story):
    pass


class Story(Base[models.Story], _type=models.Story):
    def __init__(self, story_id: int):
        self.story_id = story_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/{self.story_id}"


class StorySeasons(IdsBase[models.StorySeason, str], _type=models.StorySeason):
    suffix = "stories/seasons"


class StorySeason(Base[models.StorySeason], _type=models.StorySeason):
    def __init__(self, quest_id: str):
        self.quest_id = quest_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/seasons/{self.quest_id}"
