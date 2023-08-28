from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel


class Novelty(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/novelties
    """

    id: int
    name: str
    description: str
    icon: AnyHttpUrl
    slot: Literal[
        "Chair",
        "Music",
        "HeldItem",
        "Miscellaneous",
        "Tonic",
    ]
    unlock_item: list[int] | None = None
