import functools

from gw2 import models

from ._base import Base, IdsBase


class Achievements(IdsBase[models.Achievement, int]):
    pass


class Achievement(Base[models.Achievement]):
    def __init__(self, achievement_id: int):
        self.achievement_id = achievement_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/{self.achievement_id}"


class AchievementCategories(IdsBase[models.AchievementCategory, int]):
    suffix = "achievements/categories"


class AchievementCategory(Base[models.AchievementCategory]):
    def __init__(self, category_id: int):
        self.category_id = category_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/categories/{self.category_id}"


class AchievementGroups(IdsBase[models.AchievementGroup, str]):
    suffix = "achievements/groups"


class AchievementGroup(Base[models.AchievementGroup]):
    def __init__(self, group_id: str):
        self.group_id = group_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/groups/{self.group_id}"
