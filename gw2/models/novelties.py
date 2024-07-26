from typing import Annotated, Literal

from pydantic import AnyHttpUrl

from ..utils import EnumValidator
from ._base import BaseModel, Unknown


class Novelty(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/novelties
    """

    id: int
    name: str
    description: str
    icon: AnyHttpUrl
    slot: (
        Annotated[
            Literal[
                "Chair",
                "Music",
                "HeldItem",
                "Miscellaneous",
                "Tonic",
            ],
            EnumValidator,
        ]
        | Unknown
    )
    unlock_item: list[int] | None = None
