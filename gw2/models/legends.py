from ._base import BaseModel


class Legend(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/legends
    """

    id: str
    code: int
    swap: int
    heal: int
    elite: int
    utilities: list[int]
