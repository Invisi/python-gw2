from typing import Literal

from ._base import BaseModel

HueCategory = Literal[
    "Gray",
    "Brown",
    "Red",
    "Orange",
    "Yellow",
    "Green",
    "Blue",
    "Purple",
]
MaterialCategory = Literal[
    "Vibrant",
    "Leather",
    "Metal",
]
RarityCategory = Literal[
    "Starter",
    "Common",
    "Uncommon",
    "Rare",
    "Exclusive",
]


class ColorDetail(BaseModel):
    brightness: int
    contrast: float
    hue: int
    saturation: float
    lightness: float
    rgb: tuple[int, int, int]


class Color(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/colors
    """

    id: int
    name: str
    base_rgb: tuple[int, int, int]
    cloth: ColorDetail
    leather: ColorDetail
    metal: ColorDetail
    fur: ColorDetail | None = None
    item: int | None = None
    categories: list[HueCategory | MaterialCategory | RarityCategory]
