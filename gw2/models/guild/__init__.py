import uuid
from typing import Literal

from .._base import BaseModel


class Emblem(BaseModel):
    class Picto(BaseModel):
        id: int
        colors: list[int]

    background: Picto
    foreground: Picto
    flags: list[
        Literal[
            "FlipBackgroundHorizontal",
            "FlipBackgroundVertical",
            "FlipForegroundVertical",
            "FlipForegroundHorizontal",
        ]
    ]


class Guild(BaseModel):
    id: uuid.UUID
    name: str
    tag: str | None  # XXX: Tag can be missing too, lovely
    emblem: Emblem | None  # XXX: This should be required but is missing sometimes

    # Optional info with leader/member token
    level: int | None
    motd: str | None
    influence: int | None
    aetherium: str | None
    favor: int | None
    member_count: int | None
    member_capacity: int | None
