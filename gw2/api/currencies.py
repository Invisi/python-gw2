import functools

from gw2 import models

from ._base import Base, IdsBase


class Currencies(IdsBase[models.Currency, int]):
    pass


class Currency(Base[models.Currency]):
    def __init__(self, currency_id: int):
        self.currency_id = currency_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"currencies/{self.currency_id}"
