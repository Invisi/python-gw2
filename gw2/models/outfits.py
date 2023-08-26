from pydantic import AnyHttpUrl

from ._base import BaseModel


class Outfit(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/outfits
    """

    id: int
    icon: AnyHttpUrl
    unlock_items: list[int]
