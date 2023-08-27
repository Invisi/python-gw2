from typing import Literal

from ._base import BaseModel


class Path(BaseModel):
    id: str
    type: Literal["Story", "Explorable"]


class Dungeon(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/dungeons
    """

    id: str
    paths: list[Path]
