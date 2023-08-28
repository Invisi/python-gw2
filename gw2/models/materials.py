from ._base import BaseModel


class Material(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/materials
    """

    id: int
    name: str
    items: list[int]
    order: int
