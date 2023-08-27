from ._base import BaseModel


class Goal(BaseModel):
    active: str
    complete: str


class Quest(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/quests
    """

    id: int
    name: str
    level: int
    story: int
    goals: list[Goal]
