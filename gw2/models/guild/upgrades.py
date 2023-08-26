import enum

from pydantic import AnyHttpUrl

from .._base import BaseModel


class Type(enum.Enum):
    ACCUMULATING_CURRENCY = "AccumulatingCurrency"
    BANK_BAG = "BankBag"
    BOOST = "Boost"
    CLAIMABLE = "Claimable"
    CONSUMABLE = "Consumable"
    DECORATION = "Decoration"
    GUILD_HALL = "GuildHall"
    GUILD_HALL_EXPEDITION = "GuildHallExpedition"
    HUB = "Hub"
    QUEUE = "Queue"
    UNLOCK = "Unlock"


class CostType(enum.Enum):
    ITEM = "Item"
    COLLECTIBLE = "Collectible"
    CURRENCY = "Currency"
    COINS = "Coins"


class Cost(BaseModel):
    type: CostType
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
    type: Type
    icon: AnyHttpUrl
    build_time: int
    required_level: int
    experience: int
    prerequisites: list[int]
    costs: list[Cost] = []
