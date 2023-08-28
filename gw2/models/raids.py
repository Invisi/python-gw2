from typing import Literal

from ._base import BaseModel


class Event(BaseModel):
    id: str
    type: Literal["Boss", "Checkpoint"]


class Wing(BaseModel):
    id: str
    events: list[Event]


class Raid(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/raids
    """

    id: str
    wings: list[Wing]
