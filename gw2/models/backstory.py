from ._base import BaseModel
from .characters import Profession, Race


class BackstoryQuestion(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/backstory/questions
    """

    id: int
    title: str
    description: str
    answers: list[str]
    order: int

    professions: list[Profession] | None = None
    races: list[Race] | None = None


class BackstoryAnswer(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/backstory/answers
    """

    id: str
    title: str
    description: str
    journal: str
    question: int

    professions: list[Profession] | None = None
    races: list[Race] | None = None
