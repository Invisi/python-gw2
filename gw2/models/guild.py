from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel


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


class GuildPermission(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/permissions
    """

    id: str
    name: str
    description: str


class Cost(BaseModel):
    type: Literal[
        "Item",
        "Collectible",
        "Currency",
        "Coins",
    ]  # todo: tagged union
    name: str | None = None  # can be missing for coins
    count: int
    item_id: int | None = None


class GuildUpgrade(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/upgrades
    """

    id: int
    name: str
    description: str
    type: Literal[
        "AccumulatingCurrency",
        "BankBag",
        "Boost",
        "Claimable",
        "Consumable",
        "Decoration",
        "GuildHall",
        "GuildHallExpedition",
        "Hub",
        "Queue",
        "Unlock",
    ]
    icon: AnyHttpUrl
    build_time: int
    required_level: int
    experience: int
    prerequisites: list[int]
    costs: list[Cost] = []
    bag_max_items: int | None = None
    bag_max_coins: int | None = None
