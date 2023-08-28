from typing import Literal

from ._base import BaseModel


class World(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/worlds
    """

    id: int
    name: str
    population: Literal[
        "Low",
        "Medium",
        "High",
        "VeryHigh",
        "Full",
    ]
