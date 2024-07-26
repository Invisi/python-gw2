from dataclasses import dataclass

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


# todo: replace | None = None with empty attribute,
#   exclude when dumping as json


@dataclass(frozen=True)
class Unknown(str):
    value: str
