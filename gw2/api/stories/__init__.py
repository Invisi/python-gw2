import functools

from gw2 import models
from gw2.api._base import Base, IdsBase


class Stories(IdsBase[models.Story, int], _type=models.Story):
    pass


class Story(Base[models.Story], _type=models.Story):
    def __init__(self, story_id: int):
        self.story_id = story_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"stories/{self.story_id}"
