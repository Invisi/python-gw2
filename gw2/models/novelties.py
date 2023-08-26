import enum

from pydantic import AnyHttpUrl

from ._base import BaseModel


class Slot(enum.Enum):
    CHAIR = "Chair"
    MUSIC = "Music"
    HELD_ITEM = "HeldItem"
    MISCELLANEOUS = "Miscellaneous"
    TONIC = "Tonic"


class Novelty(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/novelties
    """

    id: int
    name: str
    description: str
    icon: AnyHttpUrl
    slot: Slot
    unlock_item: list[int] | None = None
