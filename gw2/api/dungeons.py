import functools

from gw2 import models

from ._base import Base, StringsBase


class Dungeons(StringsBase[models.Dungeon]):
    pass


class Dungeon(Base[models.Dungeon]):
    def __init__(self, dungeon_id: str):
        self.dungeon_id = dungeon_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"dungeons/{self.dungeon_id}"
