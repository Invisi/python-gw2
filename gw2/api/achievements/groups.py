import functools

from gw2 import models

from .._base import Base, IdsBase


class AchievementGroups(
    IdsBase[models.AchievementGroup, str],
    _type=models.AchievementGroup,
):
    suffix = "achievements/groups"


class AchievementGroup(Base[models.AchievementGroup], _type=models.AchievementGroup):
    def __init__(self, group_id: str):
        self.group_id = group_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"achievements/groups/{self.group_id}"
