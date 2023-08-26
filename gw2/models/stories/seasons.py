from .._base import BaseModel


class StorySeason(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/stories/seasons
    """

    id: str
    name: str
    order: int
    stories: list[int]
