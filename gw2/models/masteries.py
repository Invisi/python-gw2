from pydantic import AnyHttpUrl

from ._base import BaseModel


class Level(BaseModel):
    name: str
    description: str
    instruction: str
    icon: AnyHttpUrl
    point_cost: int
    exp_cost: int


class Mastery(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/masteries
    """

    id: int
    name: str
    requirement: str
    order: int
    background: AnyHttpUrl
    region: str
    levels: list[Level]
