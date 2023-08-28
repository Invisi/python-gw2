from pydantic import AnyHttpUrl

from ._base import BaseModel


class Quaggan(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/quaggans"""

    id: int
    url: AnyHttpUrl
