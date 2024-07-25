import datetime
from typing import Literal

from ._base import BaseModel
from .common import Stats

Access = Literal[
    "PlayForFree",
    # Core game
    "GuildWars2",
    # Expansions
    "HeartOfThorns",
    "PathOfFire",
    "EndOfDragons",
    "SecretsOfTheObscure",
    "JanthirWilds",
]


class Account(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account
    """

    id: str
    name: str
    age: int
    world: int
    guilds: list[str]
    created: datetime.datetime
    access: list[Access]
    commander: bool

    last_modified: datetime.datetime

    # guilds scope
    guild_leader: list[str] | None = None

    # progression scope
    fractal_level: int | None = None
    daily_ap: int | None = None
    monthly_ap: int | None = None
    wvw_rank: int | None = None

    build_storage_slots: int | None = None


class Achievement(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/achievements
    """

    id: int
    done: bool

    # Optional
    bits: list[int] | None = None
    current: int | None = None
    max: int | None = None
    repeated: int | None = None
    unlocked: bool | None = None


class Finisher(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/finishers
    """

    id: int
    permanent: bool
    quantity: int | None = None


class LegendaryArmory(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/legendaryarmory
    """

    id: int
    count: int


class Luck(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/luck
    """

    id: Literal["luck"]
    value: int


class Mastery(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/masteries
    """

    id: int
    level: int | None = None


class MasteryPoints(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/mastery/points
    """

    class Total(BaseModel):
        region: Literal[
            "Central Tyria",
            "Heart of Thorns",
            "Path of Fire",
            "Icebrood Saga",
            "End of Dragons",
            "Secrets of the Obscure",
        ]
        spent: int
        earned: int

    totals: list[Total]
    unlocked: list[int]


class Material(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/materials
    """

    id: int
    category: int
    binding: Literal["Account"] | None = None
    count: int


class Progression(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/progression
    """

    id: Literal[
        "fractal_agony_impedance",
        "fractal_empowerment",
        "fractal_karmic_retribution",
        "fractal_mist_attunement",
        "luck",
    ]
    value: int


class SharedInventorySlot(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/inventory
    """

    # seems to be only slightly different from a regular
    # inventory slot

    id: int
    count: int

    binding: Literal["Account"] | None = None
    charges: int | None = None
    dyes: list[int] | None = None
    infusions: list[int] | None = None
    skin: int | None = None
    stats: Stats | None = None
    upgrade_slot_indices: list[int] | None = None
    upgrades: list[int] | None = None


class WalletEntry(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/wallet
    """

    id: int
    value: int
