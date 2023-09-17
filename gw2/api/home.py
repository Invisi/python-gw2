import functools

from gw2 import models

from ._base import Base, IdsBase, StringsBase


class HomeCats(IdsBase[models.HomeCat, int]):
    suffix = "home/cats"


class HomeCat(Base[models.HomeCat]):
    def __init__(self, cat_id: int):
        self.cat_id = cat_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"home/cats/{self.cat_id}"


class HomeNodes(StringsBase[models.HomeNode]):
    suffix = "home/nodes"


class HomeNode(Base[models.HomeNode]):
    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"home/nodes/{self.node_id}"
