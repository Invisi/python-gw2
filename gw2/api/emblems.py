import functools

from gw2 import models

from ._base import Base, IdsBase


class EmblemBackgrounds(IdsBase[models.Emblem, int], _type=models.Emblem):
    suffix = "emblem/backgrounds"


class EmblemBackground(Base[models.Emblem], _type=models.Emblem):
    def __init__(self, emblem_id: int):
        self.emblem_id = emblem_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"emblem/backgrounds/{self.emblem_id}"


class EmblemForegrounds(IdsBase[models.Emblem, int], _type=models.Emblem):
    suffix = "emblem/foregrounds"


class EmblemForeground(Base[models.Emblem], _type=models.Emblem):
    def __init__(self, emblem_id: int):
        self.emblem_id = emblem_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"emblem/foregrounds/{self.emblem_id}"
