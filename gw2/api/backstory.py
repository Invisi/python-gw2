import functools

from gw2 import models

from ._base import Base, IdsBase


class BackstoryQuestions(IdsBase[models.BackstoryQuestion, str]):
    suffix = "backstory/questions"


class BackstoryQuestion(Base[models.BackstoryQuestion]):
    def __init__(self, upgrade_id: int):
        self.upgrade_id = upgrade_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"backstory/questions/{self.upgrade_id}"


class BackstoryAnswers(
    IdsBase[models.BackstoryAnswer, str],
):
    suffix = "backstory/answers"


class BackstoryAnswer(Base[models.BackstoryAnswer]):
    def __init__(self, backstory_id: str):
        self.backstory_id = backstory_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"backstory/answers/{self.backstory_id}"
