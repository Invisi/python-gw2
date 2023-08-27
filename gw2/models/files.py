from pydantic import AnyHttpUrl

from ._base import BaseModel


class File(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/files
    """

    id: str
    icon: AnyHttpUrl
