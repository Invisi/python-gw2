import functools

from gw2 import models

from ._base import Base, IdsBase


class Quests(IdsBase[models.Quest, int]):
    pass


class Quest(Base[models.Quest]):
    def __init__(self, quest_id: int):
        self.quest_id = quest_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"quests/{self.quest_id}"
