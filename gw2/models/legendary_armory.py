from ._base import BaseModel


class LegendaryArmory(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/legendaryarmory
    """

    id: int
    max_count: int
