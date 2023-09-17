import functools

from gw2 import models

from ._base import AllIdsBase, Base


class Files(AllIdsBase[models.File, str]):
    pass


class File(Base[models.File]):
    def __init__(self, file_id: str):
        self.file_id = file_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"files/{self.file_id}"
