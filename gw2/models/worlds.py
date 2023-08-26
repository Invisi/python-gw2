import enum

from ._base import BaseModel


class Population(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    VERY_HIGH = "VeryHigh"
    FULL = "Full"


class World(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/worlds
    """

    id: int
    name: str
    population: Population
