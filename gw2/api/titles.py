import functools

from gw2 import models

from ._base import Base, IdsBase


class Titles(IdsBase[models.Title, int]):
    pass


class Title(Base[models.Title]):
    def __init__(self, title_id: int):
        self.title_id = title_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"titles/{self.title_id}"
