import datetime
import enum

from ._base import BaseModel


class Language(enum.Enum):
    ENGLISH = "en"
    SPANISH = "es"
    GERMAN = "de"
    FRENCH = "fr"
    CHINESE = "zh"


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

    langs: list[Language]
    routes: list[Route]
    schema_versions: list[SchemaVersion]
