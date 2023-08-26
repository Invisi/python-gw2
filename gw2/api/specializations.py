import functools

from gw2 import models

from ._base import Base, IdsBase


class Specializations(IdsBase[models.Specialization, int], _type=models.Specialization):
    pass


class Specialization(Base[models.Specialization], _type=models.Specialization):
    def __init__(self, spec_id: int):
        self.spec_id = spec_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"specializations/{self.spec_id}"
