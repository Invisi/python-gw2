from typing import Annotated, Literal

from ..utils import EnumValidator
from . import Unknown
from ._base import BaseModel


class WizardsVaultListing(BaseModel):
    id: int
    item_id: int
    item_count: int
    type: Annotated[Literal["Legacy", "Featured", "Normal"], EnumValidator] | Unknown
    cost: int


class WizardsVaultObjective(BaseModel):
    id: int
    title: str
    track: Annotated[Literal["PvE", "PvP", "WvW"], EnumValidator] | Unknown
    acclaim: int
