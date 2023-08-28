from .._base import BaseModel


class GuildPermission(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/permissions
    """

    id: str
    name: str
    description: str
