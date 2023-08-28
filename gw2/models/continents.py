import uuid
from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import Region as RegionType

Coordinates = tuple[float, float]
Rectangle = tuple[tuple[float, float], tuple[float, float]]
Bounds = list[tuple[float, float]]


class Continent(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/continents
    """

    id: int
    name: str
    continent_dims: tuple[int, int]
    min_zoom: int
    max_zoom: int
    floors: list[int]


class Floor(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/continents
    """

    id: int
    texture_dims: tuple[int, int]
    clamped_view: list[tuple[int, int]] | None = None
    regions: dict[int, "Region"]


class Region(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/continents
    """

    id: int
    name: str
    label_coord: Coordinates
    continent_rect: Rectangle
    maps: dict[int, "ContinentMap"]


class ContinentMap(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/continents
    """

    id: int
    name: str
    min_level: int
    max_level: int
    default_floor: int
    label_coord: Coordinates | None = None
    map_rect: Rectangle
    continent_rect: Rectangle
    points_of_interest: dict[int, "PointOfInterest"]
    tasks: dict[int, "Task"]
    skill_challenges: list["SkillChallenge"]
    sectors: dict[int, "Sector"]
    adventures: list["Adventure"]
    mastery_points: list["MasteryPoint"]
    god_shrines: list["GodShrine"] | None = None


class PointOfInterest(BaseModel):
    id: int
    name: str | None = None  # missing on e.g. vistas
    type: Literal["landmark", "waypoint", "vista", "unlock"]
    floor: int
    coord: Coordinates
    chat_link: str
    icon: AnyHttpUrl | None = None


class Task(BaseModel):
    id: int
    objective: str
    level: int
    coord: Coordinates
    bounds: Bounds
    chat_link: str


class SkillChallenge(BaseModel):
    id: str | None = None
    coord: Coordinates


class Sector(BaseModel):
    id: int
    name: str | None = None
    level: int
    coord: Coordinates
    bounds: Bounds
    chat_link: str


class Adventure(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    coord: Coordinates


class MasteryPoint(BaseModel):
    id: int
    coord: Coordinates
    region: RegionType


class GodShrine(BaseModel):
    id: int
    name: str
    name_contested: str
    coord: Coordinates
    poi_id: int
    icon: AnyHttpUrl
    icon_contested: AnyHttpUrl
