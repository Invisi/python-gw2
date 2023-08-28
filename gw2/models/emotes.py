from ._base import BaseModel


class Emote(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/emotes
    """

    id: str
    commands: list[str]
    unlock_items: list[int]
