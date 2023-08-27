from pydantic import AnyHttpUrl

from ._base import BaseModel


class Mini(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/minis
    """

    id: int
    name: str
    unlock: str | None = None
    icon: AnyHttpUrl
    order: int
    item_id: int
