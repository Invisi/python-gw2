import functools

from gw2 import models

from ._base import Base, IdsBase, StringsBase


class MountSkins(IdsBase[models.MountSkin, int]):
    suffix = "mounts/skins"


class MountSkin(Base[models.MountSkin]):
    def __init__(self, skin_id: int):
        self.skin_id = skin_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"mounts/skins/{self.skin_id}"


class MountTypes(StringsBase[models.MountType]):
    suffix = "mounts/types"


class MountType(Base[models.MountType]):
    def __init__(self, type_id: str):
        self.type_id = type_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"mounts/types/{self.type_id}"
