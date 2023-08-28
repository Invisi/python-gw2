import functools

from gw2 import models

from ._base import Base, IdsBase


class Raids(IdsBase[models.Raid, int], _type=models.Raid):
    pass


class Raid(Base[models.Raid], _type=models.Raid):
    def __init__(self, raid_id: str):
        self.raid_id = raid_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"raids/{self.raid_id}"
