from pydantic import AnyHttpUrl

from ._base import BaseModel
from .common import DyeSlot, SkillSlot


class MountSkin(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/mounts/skins
    """

    id: int
    name: str
    icon: AnyHttpUrl
    mount: str
    dye_slots: list[DyeSlot]


class Skill(BaseModel):
    id: int
    slot: SkillSlot


class MountType(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/mounts/types
    """

    id: str
    name: str
    default_skin: int
    skins: list[int]
    skills: list[Skill]
