from pydantic import AnyHttpUrl

from .._base import BaseModel


class AchievementCategory(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/achievements/categories
    """

    # todo: upgrade schema to 2022-03-23 for extended data

    id: int
    name: str
    description: str
    order: int
    icon: AnyHttpUrl
    achievements: list[int]
