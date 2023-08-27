from pydantic import AnyHttpUrl

from ._base import BaseModel


class Emblem(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/emblem/backgrounds
    https://wiki.guildwars2.com/wiki/API:2/emblem/foregrounds
    """

    id: int
    layers: list[AnyHttpUrl]
