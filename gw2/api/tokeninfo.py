from gw2 import models
from gw2.api._base import Base


class TokenInfo(Base[models.TokenInfo], _type=models.TokenInfo):
    pass
