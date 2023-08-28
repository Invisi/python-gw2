from pydantic import AnyHttpUrl

from ._base import BaseModel


class MailCarrier(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/mailcarriers
    """

    id: int
    unlock_items: list[int]
    order: int
    icon: AnyHttpUrl
    name: str
    flags: list[str]  # usually empty
