from gw2 import models

from .._base import Base, ListBase


class Account(Base[models.Account], _type=models.Account):
    def achievements(self) -> "Achievements":
        client = Achievements()
        client.auth(self.api_key)
        return client


class Achievements(
    ListBase[models.account.Achievement],
    _type=models.account.Achievement,
):
    suffix = "account/achievements"
