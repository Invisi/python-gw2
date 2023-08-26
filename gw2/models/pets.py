from pydantic import AnyHttpUrl

from ._base import BaseModel


class Pet(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pets
    """

    id: int
    name: str
    icon: AnyHttpUrl
    unlock_items: list[int] | None = None
