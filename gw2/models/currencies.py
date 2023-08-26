from ._base import BaseModel


class Currency(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/currencies
    """

    id: int
    name: str
    description: str
    icon: str
    order: int
