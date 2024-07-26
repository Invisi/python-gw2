import datetime
from typing import Annotated, Literal

from pydantic import AnyHttpUrl

from ..utils import EnumValidator
from . import common, pvp
from ._base import BaseModel, Unknown

GuildPermissionId = (
    Annotated[
        Literal[
            "ClaimableEditOptions",
            "EditBGM",
            "ActivatePlaceables",
            "DepositItemsTrove",
            "WithdrawItemsStash",
            "WithdrawItemsTrove",
            "EditAssemblyQueue",
            "WithdrawCoinsStash",
            "ActivateWorldEvent",
            "PlaceArenaDecoration",
            "DepositItemsStash",
            "EditMonument",
            "StartingRole",
            "SpendFuel",
            "TeamAdmin",
            "EditRoles",
            "Admin",
            "WithdrawCoinsTrove",
            "DepositCoinsTrove",
            "PurchaseUpgrades",
            "EditEmblem",
            "ClaimableActivate",
            "MissionControl",
            "OpenPortal",
            "SetGuildHall",
            "DepositCoinsStash",
            "PlaceDecoration",
            "ClaimableSpend",
            "EditMOTD",
            "EditAnthem",
            "DecorationAdmin",
            "ClaimableClaim",
        ],
        EnumValidator,
    ]
    | Unknown
)


class Emblem(BaseModel):
    class Picto(BaseModel):
        id: int
        colors: list[int]

    background: Picto
    foreground: Picto
    flags: list[
        Literal[
            "FlipBackgroundHorizontal",
            "FlipBackgroundVertical",
            "FlipForegroundVertical",
            "FlipForegroundHorizontal",
        ]
    ]


class Guild(BaseModel):
    id: str
    name: str
    tag: str | None = None  # XXX: Tag can be missing too, lovely
    emblem: Emblem | None = (
        None  # XXX: This should be required but is missing sometimes
    )


class AuthenticatedGuild(Guild):
    # Optional info with leader/member token
    level: int
    motd: str
    influence: int
    aetherium: int
    resonance: int
    favor: int
    member_count: int
    member_capacity: int


class GuildPermission(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/permissions
    """

    id: GuildPermissionId
    name: str
    description: str


class Cost(BaseModel):
    type: Literal[
        "Item",
        "Collectible",
        "Currency",
        "Coins",
    ]  # todo: tagged union
    name: str | None = None  # can be missing for coins
    count: int
    item_id: int | None = None


class GuildUpgrade(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/upgrades
    """

    id: int
    name: str
    description: str
    type: Literal[
        "AccumulatingCurrency",
        "BankBag",
        "Boost",
        "Claimable",
        "Consumable",
        "Decoration",
        "GuildHall",
        "GuildHallExpedition",
        "Hub",
        "Queue",
        "Unlock",
    ]
    icon: AnyHttpUrl
    build_time: int
    required_level: int
    experience: int
    prerequisites: list[int]
    costs: list[Cost] = []
    bag_max_items: int | None = None
    bag_max_coins: int | None = None


class Log:
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/log
    """

    class _Base(BaseModel):
        id: int
        time: datetime.datetime
        user: str | None = None
        type: (
            Annotated[
                Literal[
                    "joined",
                    "invited",
                    "kick",
                    "invite_declined",
                    "rank_change",
                    "treasury",
                    "stash",
                    "motd",
                    "upgrade",
                    "influence",
                ],
                EnumValidator,
            ]
            | Unknown
        )

    class Invite(_Base):
        invited_by: str

    class InviteDeclined(_Base):
        declined_by: str

    class Join(_Base):
        user: str

    class Kick(_Base):
        kicked_by: str

    class Motd(_Base):
        motd: str

    class RankChange(_Base):
        # may be missing if guild was created by user
        # old_rank seems to be "none" in such a case
        changed_by: str | None = None
        old_rank: str
        new_rank: str

    class Stash(_Base):
        operation: Literal["deposit", "withdraw", "move"]
        item_id: int
        count: int
        coins: int

    class Treasury(_Base):
        item_id: int
        count: int

    class Upgrade(_Base):
        action: Literal["queued", "cancelled", "complete", "completed", "sped_up"]
        count: int | None = None
        item_id: int | None = None
        recipe_id: int | None = None  # always optional
        upgrade_id: int

    class Influence(_Base):
        activity: Literal["gifted", "daily_login"]
        participants: list[str] | None = None  # list of account names
        total_participants: int | None = None


class Member(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/members
    """

    name: str
    rank: str
    joined: datetime.datetime


class Rank(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/ranks
    """

    id: str
    order: int
    permissions: list[GuildPermissionId]
    icon: AnyHttpUrl


class InventorySlot(BaseModel):
    id: int
    count: int


class Stash(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/stash
    """

    upgrade_id: int
    size: int
    coins: int
    note: str | None = None
    inventory: list[InventorySlot | None]


class Storage(InventorySlot):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/storage
    """


class Team(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/teams
    """

    class Member(BaseModel):
        name: str
        role: Literal["Captain", "Member"]

    class Season(BaseModel):
        id: str
        wins: int
        losses: int
        rating: int

    id: int
    members: list[Member]
    name: str
    state: (  # todo: other states are unknown
        Annotated[Literal["Active"], EnumValidator] | Unknown
    )
    aggregate: pvp.WinLoss
    ladders: pvp.Ladders | common.EmptyObject
    games: list[pvp.Game]
    seasons: list[Season] | None = None


class Treasury(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/guild/:id/treasury
    """

    class Upgrade(BaseModel):
        upgrade_id: int
        count: int

    item_id: int
    count: int
    needed_by: list[Upgrade]
