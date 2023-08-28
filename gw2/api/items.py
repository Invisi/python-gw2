import functools

from gw2 import models

from ._base import Base, IdsBase


class Items(IdsBase[models.Item, int], _type=models.Item):
    pass


class Item(Base[models.Item], _type=models.Item):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"items/{self.item_id}"
