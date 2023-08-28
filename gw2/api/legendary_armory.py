import functools

from gw2 import models

from ._base import Base, IdsBase


class LegendaryArmory(
    IdsBase[models.LegendaryArmory, int], _type=models.LegendaryArmory
):
    pass


class LegendaryArmoryItem(Base[models.LegendaryArmory], _type=models.LegendaryArmory):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"legendaryarmory/{self.item_id}"
