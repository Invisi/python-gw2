import functools

from gw2 import models

from ._base import Base, IdsBase


class Novelties(IdsBase[models.Novelty, int]):
    pass


class Novelty(Base[models.Novelty]):
    def __init__(self, novelty_id: int):
        self.novelty_id = novelty_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"novelties/{self.novelty_id}"
