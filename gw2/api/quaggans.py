import functools

from gw2 import models

from ._base import Base, StringsBase


class Quaggans(StringsBase[models.Quaggan]):
    pass


class Quaggan(Base[models.Quaggan]):
    def __init__(self, quaggan_id: str):
        self.quaggan_id = quaggan_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"quaggans/{self.quaggan_id}"
