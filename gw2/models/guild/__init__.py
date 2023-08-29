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
    id: str
    name: str
    tag: str | None = None  # XXX: Tag can be missing too, lovely
    emblem: Emblem | None = (
        None  # XXX: This should be required but is missing sometimes
    )

    # Optional info with leader/member token
    level: int | None = None
    motd: str | None = None
    influence: int | None = None
    aetherium: str | None = None
    favor: int | None = None
    member_count: int | None = None
    member_capacity: int | None = None
