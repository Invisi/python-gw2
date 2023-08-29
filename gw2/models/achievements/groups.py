from .._base import BaseModel


class AchievementGroup(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements/groups
    """

    id: str
    name: str
    description: str
    order: int
    categories: list[int]
