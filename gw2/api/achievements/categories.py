import functools

from gw2 import models

from .._base import Base, IdsBase


class AchievementCategories(
    IdsBase[models.AchievementCategory, int],
    _type=models.AchievementCategory,
):
    suffix = "achievements/categories"


class AchievementCategory(
    Base[models.AchievementCategory],
    _type=models.AchievementCategory,
):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/categories/{self.category_id}"
