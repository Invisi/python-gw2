import datetime
import uuid
from typing import List, Literal, Optional

from gw2.models._base import BaseModel


class TokenInfo(BaseModel):
    id: uuid.UUID
    name: str
    permissions: List[
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
    expires_at: Optional[datetime.datetime]
    issued_at: Optional[datetime.datetime]
    urls: Optional[List[str]]
