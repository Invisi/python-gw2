from typing import List, Optional

from ._base import BaseModel
from .characters import Profession, Race


class BackstoryQuestions(BaseModel):
    id: int
    title: str
    description: str
    answers: List[str]
    order: int

    professions: Optional[List[Profession]]
    races: Optional[List[Race]]


class BackstoryAnswers(BaseModel):
    id: str
    title: str
    description: str
    journal: str
    question: int

    professions: Optional[List[Profession]]
    races: Optional[List[Race]]
