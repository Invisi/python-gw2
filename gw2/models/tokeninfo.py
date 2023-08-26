import datetime
import uuid
from typing import Literal

from ._base import BaseModel


class TokenInfo(BaseModel):
    id: uuid.UUID
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
        ]
    ]
    type: Literal["APIKey", "Subtoken"]

    # Following fields only exist on subtokens
    expires_at: datetime.datetime | None
    issued_at: datetime.datetime | None
    urls: list[str] | None
