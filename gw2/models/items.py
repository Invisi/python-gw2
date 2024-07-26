from typing import Annotated, Literal

from pydantic import AnyHttpUrl, BeforeValidator

from ..utils import EnumValidator
from ._base import BaseModel, Unknown
from .common import (
    Attribute,
    Gender,
    Profession,
    Race,
    Rarity,
    Weapon,
    WeaponDamage,
)
from .skins import GatheringType

Type = (
    Annotated[
        Literal[
            "Armor",
            "Back",
            "Bag",
            "Consumable",
            "Container",
            "CraftingMaterial",
            "Gathering",
            "Gizmo",
            "JadeTechModule",
            "Key",
            "MiniPet",
            "PowerCore",
            "Tool",
            "Trait",
            "Trinket",
            "Trophy",
            "UpgradeComponent",
            "Weapon",
            "Relic",
        ],
        EnumValidator,
    ]
    | Unknown
)


Flag = (
    Annotated[
        Literal[
            "AccountBindOnUse",
            "AccountBound",
            "Attuned",
            "BulkConsume",
            "DeleteWarning",
            "HideSuffix",
            "Infused",
            "MonsterOnly",
            "NoMysticForge",
            "NoSalvage",
            "NoSell",
            "NoUnderwater",
            "NotUpgradeable",
            "SoulbindOnAcquire",
            "SoulBindOnUse",
            "Tonic",
            "Unique",
        ],
        EnumValidator,
    ]
    | Unknown
)


GameType = Literal[
    "Activity",
    "Dungeon",
    "Pve",
    "Pvp",
    "PvpLobby",
    "Wvw",
]


class Upgrade(BaseModel):
    upgrade: Literal["Attunement", "Infusion"]
    item_id: int


class AttributeDetails(BaseModel):
    attribute: Attribute
    modifier: int


class Buff(BaseModel):
    skill_id: int
    description: str | None = None


class InfixUpgrade(BaseModel):
    id: int
    attributes: list[AttributeDetails]
    buff: Buff | None = None


class InfusionSlot(BaseModel):
    flags: list[Literal["Enrichment", "Infusion"]]
    item_id: int | None = None


class Details:
    class Armor(BaseModel):
        type: Literal[
            "Boots",
            "Coat",
            "Gloves",
            "Helm",
            "HelmAquatic",
            "Leggings",
            "Shoulders",
        ]
        weight_class: Literal["Clothing", "Light", "Medium", "Heavy"]
        defense: int
        infusion_slots: list[InfusionSlot]
        attribute_adjustment: float
        infix_upgrade: InfixUpgrade | None = None
        suffix_item_id: int | None = None
        secondary_suffix_item_id: int | None = None
        stat_choices: list[int] | None = None

    class BackItem(BaseModel):
        infusion_slots: list[InfusionSlot]
        attribute_adjustment: float
        infix_upgrade: InfixUpgrade | None = None
        suffix_item_id: int | None = None
        secondary_suffix_item_id: int | None = None
        stat_choices: list[int] | None = None

    class Bag(BaseModel):
        size: int
        no_sell_or_sort: bool

    class Consumable(BaseModel):
        type: Literal[
            "AppearanceChange",
            "Booze",
            "ContractNpc",
            "Currency",
            "Food",
            "Generic",
            "Halloween",
            "Immediate",
            "MountRandomUnlock",
            "RandomUnlock",
            "Transmutation",
            "Unlock",
            "UpgradeRemoval",
            "Utility",
            "TeleportToFriend",
        ]
        description: str | None = None
        duration_ms: int | None = None
        unlock_type: (
            Annotated[
                Literal[
                    "BagSlot",
                    "BankTab",
                    "BuildLibrarySlot",
                    "BuildLoadoutTab",
                    "Champion",
                    "CollectibleCapacity",
                    "Content",
                    "CraftingRecipe",
                    "Dye",
                    "JadeBotSkin",
                    "GearLoadoutTab",
                    "GliderSkin",
                    "Minipet",
                    "Ms",
                    "Outfit",
                    "RandomUnlock",
                    "SharedSlot",
                ],
                EnumValidator,
            ]
            | Unknown
        ) | None = None
        color_id: int | None = None
        recipe_id: int | None = None
        extra_recipe_ids: list[int] | None = None
        apply_count: int | None = None
        name: str | None = None
        icon: AnyHttpUrl | None = None
        skins: list[int] | None = None
        guild_upgrade_id: int | None = None

    class Container(BaseModel):
        type: Literal["Default", "GiftBox", "Immediate", "OpenUI"]

    class Gizmo(BaseModel):
        type: Literal[
            "Default",
            "ContainerKey",
            "RentableContractNpc",
            "UnlimitedConsumable",
        ]
        guild_upgrade_id: int | None = None
        vendor_ids: list[int] | None = None

    class Miniature(BaseModel):
        minipet_id: int

    class SalvageKit(BaseModel):
        type: Literal["Salvage"]
        charges: int

    class Trinket(BaseModel):
        type: Literal["Accessory", "Amulet", "Ring"]
        infusion_slots: list[InfusionSlot]
        attribute_adjustment: float
        infix_upgrade: InfixUpgrade | None = None
        suffix_item_id: int | None = None
        secondary_suffix_item_id: int | None = None
        stat_choices: list[int] | None = None

    class UpgradeComponent(BaseModel):
        attribute_adjustment: float
        bonuses: list[str] | None = None
        flags: list[
            Weapon | Literal["HeavyArmor", "MediumArmor", "LightArmor", "Trinket"]
        ]
        infix_upgrade: InfixUpgrade
        infusion_upgrade_flags: list[Literal["Enrichment", "Infusion"]]
        suffix: str
        type: Literal["Default", "Gem", "Rune", "Sigil"]

    class Weapon(BaseModel):
        type: Weapon
        damage_type: WeaponDamage
        min_power: int
        max_power: int
        defense: int
        infusion_slots: list[InfusionSlot]
        attribute_adjustment: float
        infix_upgrade: InfixUpgrade | None = None
        suffix_item_id: int | None = None
        secondary_suffix_item_id: Annotated[
            int | None,
            BeforeValidator(
                # XXX: shim for items like 28208,
                # where secondary_suffix_item_id is ""
                lambda x: None if x == "" else x
            ),
        ] = None
        stat_choices: list[int] | None = None

    class Gathering(BaseModel):
        # todo: missing on wiki
        type: GatheringType


class Item(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/items
    """

    id: int
    chat_link: str
    name: str
    icon: AnyHttpUrl | None = None
    description: str | None = None
    type: Type
    rarity: Rarity
    level: int
    vendor_value: int
    default_skin: int | None = None
    flags: list[Flag]
    game_types: list[GameType]
    restrictions: list[Race | Profession | Gender]
    upgrades_into: list[Upgrade] | None = None
    upgrades_from: list[Upgrade] | None = None
    details: (
        Details.Armor
        | Details.BackItem
        | Details.Bag
        | Details.Consumable
        | Details.Container
        | Details.Gathering
        | Details.Gizmo
        | Details.Miniature
        | Details.SalvageKit
        | Details.Trinket
        | Details.UpgradeComponent
        | Details.Weapon
        | None
    ) = None
