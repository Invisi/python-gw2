import functools

from gw2 import models

from ._base import Base, IdsBase


class MailCarriers(IdsBase[models.MailCarrier, str], _type=models.MailCarrier):
    pass


class MailCarrier(Base[models.MailCarrier], _type=models.MailCarrier):
    def __init__(self, carrier_id: int):
        self.carrier_id = carrier_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"mailcarriers/{self.carrier_id}"
