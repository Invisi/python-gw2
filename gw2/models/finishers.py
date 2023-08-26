from pydantic import AnyHttpUrl

from ._base import BaseModel


class Finisher(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/finishers
    """

    id: int
    unlock_details: str
    unlock_items: list[int] | None = None
    order: int
    icon: AnyHttpUrl
    name: str
