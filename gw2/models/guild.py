import uuid
from typing import List, Literal, Optional

from ._base import BaseModel


class Emblem(BaseModel):
    class Picto(BaseModel):
        id: int
        colors: List[int]

    background: Picto
    foreground: Picto
    flags: List[
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
    tag: str
    emblem: Optional[Emblem]  # XXX: This should be required but is missing sometimes

    # Optional info with leader/member token
    level: Optional[int]
    motd: Optional[str]
    influence: Optional[int]
    aetherium: Optional[str]
    favor: Optional[int]
    member_count: Optional[int]
    member_capacity: Optional[int]
