from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import Profession


class Specialization(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/specializations
    """

    id: int
    background: AnyHttpUrl
    elite: bool
    icon: AnyHttpUrl
    major_traits: list[int]
    minor_traits: list[int]
    name: str
    profession: Profession
    profession_icon: AnyHttpUrl | None = None
    profession_icon_big: AnyHttpUrl | None = None
    weapon_trait: int | None = None
