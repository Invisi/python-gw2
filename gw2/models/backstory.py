from ._base import BaseModel
from .characters import Profession, Race


class BackstoryQuestions(BaseModel):
    id: int
    title: str
    description: str
    answers: list[str]
    order: int

    professions: list[Profession] | None
    races: list[Race] | None


class BackstoryAnswers(BaseModel):
    id: str
    title: str
    description: str
    journal: str
    question: int

    professions: list[Profession] | None
    races: list[Race] | None
