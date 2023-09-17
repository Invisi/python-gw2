from gw2 import models

from ._base import Base


class TokenInfo(
    Base[models.TokenInfo | models.SubTokenInfo],
):
    pass
