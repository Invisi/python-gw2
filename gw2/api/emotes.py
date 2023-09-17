import functools

from gw2 import models

from ._base import Base, IdsBase


class Emotes(IdsBase[models.Emote, int]):
    pass


class Emote(Base[models.Emote]):
    def __init__(self, emote_id: str):
        self.emote_id = emote_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"emotes/{self.emote_id}"
