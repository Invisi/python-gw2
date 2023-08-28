from typing import Literal

from ._base import BaseModel
from .continents import Coordinates, Rectangle


class Map(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/maps
    """

    id: int
    name: str
    min_level: int
    max_level: int
    default_floor: int
    label_coord: Coordinates | None = None
    map_rect: Rectangle
    continent_rect: Rectangle
    # different from ContinentMap
    type: Literal[
        "BlueHome",
        "Center",
        "EdgeOfTheMists",
        "GreenHome",
        "Instance",
        "JumpPuzzle",
        "Public",
        "Pvp",
        "RedHome",
        "Tutorial",
        "Unknown",
    ]
    floors: list[int]
    region_id: int | None = None
    region_name: str | None = None
    continent_id: int | None = None
    continent_name: str | None = None
