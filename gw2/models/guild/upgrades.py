from typing import Literal

from pydantic import AnyHttpUrl

from .._base import BaseModel


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
