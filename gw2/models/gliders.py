from pydantic import AnyHttpUrl

from ._base import BaseModel


class Glider(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/gliders
    """

    id: int
    unlock_items: list[int] | None = None
    order: int
    icon: AnyHttpUrl
    name: str
    description: str
    default_dyes: list[int]
