import functools

from gw2 import models

from .._base import Base, StringsBase


class GuildPermissions(
    StringsBase[models.GuildPermission], _type=models.GuildPermission
):
    suffix = "guild/permissions"


class GuildPermission(Base[models.GuildPermission], _type=models.GuildPermission):
    def __init__(self, permission_id: str):
        self.permission_id = permission_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"guild/permissions/{self.permission_id}"
