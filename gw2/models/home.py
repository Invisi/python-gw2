from ._base import BaseModel


class HomeCat(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/home/cats
    """

    id: int
    hint: str


class HomeNode(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/home/nodes
    """

    id: str
