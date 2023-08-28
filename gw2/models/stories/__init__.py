import enum
from typing import Literal

from .._base import BaseModel
from ..common import Race


class Chapter(BaseModel):
    name: str


class Story(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/stories
    """

    id: int
    season: str  # uuid
    name: str
    description: str
    timeline: str
    level: int
    order: int
    chapters: list[Chapter]
    races: list[Race] | None = None
    flags: list[Literal["RequiresUnlock"]] | None = None
