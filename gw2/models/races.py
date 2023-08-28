from ._base import BaseModel


class Race(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/races
    """

    id: str
    name: str
    skills: list[int]
