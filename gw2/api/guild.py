import functools

from ._base import Base
from gw2 import models


class Guild(Base[models.Guild], _type=models.Guild):
    def __init__(self, guild_id: str):
        self.guild_id = guild_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/{self.guild_id}"
