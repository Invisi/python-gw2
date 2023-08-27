from ._base import BaseModel


class Build(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/build
    """

    id: int


class BuildManifest(BaseModel):
    build_id: int
    exe_id: int
    exe_size: int
    manifest_id: int
    manifest_size: int
