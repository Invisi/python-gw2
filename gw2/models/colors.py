import enum

from ._base import BaseModel


class ColorDetail(BaseModel):
    brightness: int
    contrast: float
    hue: int
    saturation: float
    lightness: float
    rgb: tuple[int, int, int]


class HueCategory(enum.Enum):
    GRAY = "Gray"
    BROWN = "Brown"
    RED = "Red"
    ORANGE = "Orange"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    PURPLE = "Purple"


class MaterialCategory(enum.Enum):
    VIBRANT = "Vibrant"
    LEATHER = "Leather"
    METAL = "Metal"


class RarityCategory(enum.Enum):
    STARTER = "Starter"
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EXCLUSIVE = "Exclusive"


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
