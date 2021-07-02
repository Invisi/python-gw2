from gw2 import models
from gw2.api._base import Base, ListBase


class Account(Base[models.Account], _type=models.Account):
    pass


class Achievements(
    ListBase[models.account.Achievement], _type=models.account.Achievement
):
    suffix = "account/achievements"
