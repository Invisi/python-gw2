import datetime
from typing import Literal

from ._base import BaseModel


class TokenInfo(BaseModel):
    id: str
    name: str
    permissions: list[
        Literal[
            "account",
            "builds",
            "characters",
            "guilds",
            "inventories",
            "progression",
            "pvp",
            "tradingpost",
            "unlocks",
            "wallet",
            "wvw",
        ]
    ]
    type: Literal["APIKey", "Subtoken"]


class SubTokenInfo(BaseModel):
    # Following fields only exist on subtokens
    expires_at: datetime.datetime | None
    issued_at: datetime.datetime | None
    urls: list[str] | None
