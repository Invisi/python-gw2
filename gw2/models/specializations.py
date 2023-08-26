from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import Profession


class Specialization(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/specializations
    """

    id: int
    name: str
    profession: Profession
    elite: bool
    icon: AnyHttpUrl
    background: AnyHttpUrl
    minor_traits: list[int]
    major_traits: list[int]
