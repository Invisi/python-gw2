from ._base import BaseModel


class Attribute(BaseModel):
    attribute: str
    multiplier: float
    value: int


class ItemStat(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/itemstats
    """

    id: int
    name: str
    attributes: list[Attribute]
