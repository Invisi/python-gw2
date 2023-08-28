from pydantic import AnyHttpUrl

from ._base import BaseModel


class Skill(BaseModel):
    id: int


class Pet(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/pets
    """

    id: int
    name: str
    description: str
    icon: AnyHttpUrl
    unlock_items: list[int] | None = None
    skills: list[Skill] | None = None
