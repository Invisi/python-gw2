import functools

from gw2 import models

from ._base import Base, IdsBase


class Materials(IdsBase[models.Material, int]):
    pass


class Material(Base[models.Material]):
    def __init__(self, material_id: int):
        self.material_id = material_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"materials/{self.material_id}"
