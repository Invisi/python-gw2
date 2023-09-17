import functools

from gw2 import models

from ._base import Base, IdsBase


class Legends(IdsBase[models.Legend, int]):
    pass


class Legend(Base[models.Legend]):
    def __init__(self, legend_id: str):
        self.legend_id = legend_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"legends/{self.legend_id}"
