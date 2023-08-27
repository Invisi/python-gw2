from ._base import BaseModel


class Title(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/titles
    """

    id: int
    name: str
    achievement: int | None = None
    achievements: list[int] | None = None
    ap_required: int | None = None
