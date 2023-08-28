import datetime
from typing import Literal

from ._base import BaseModel


class Route(BaseModel):
    path: str
    lang: bool
    auth: bool
    active: bool


class SchemaVersion(BaseModel):
    v: datetime.datetime
    desc: str


class V2(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2
    """

    langs: list[
        Literal[
            "en",
            "es",
            "de",
            "fr",
            "zh",
        ]
    ]
    routes: list[Route]
    schema_versions: list[SchemaVersion]
