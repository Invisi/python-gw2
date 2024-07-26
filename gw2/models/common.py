from typing import Annotated, Literal

from pydantic import AnyHttpUrl, Field

from ..utils import EnumValidator
from ._base import BaseModel, Unknown

Rarity = Literal[
    "Junk",
    "Basic",
    "Fine",
    "Masterwork",
    "Rare",
    "Exotic",
    "Ascended",
    "Legendary",
]

Attunement = Literal[
    "Fire",
    "Water",
    "Air",
    "Earth",
]

Race = Literal[
    "Asura",
    "Charr",
    "Human",
    "Norn",
    "Sylvari",
]
Gender = Literal["Female", "Male"]
Profession = Literal[
    "Elementalist",
    "Engineer",
    "Guardian",
    "Mesmer",
    "Necromancer",
    "Ranger",
    "Revenant",
    "Thief",
    "Warrior",
]
Discipline = Literal[
    "Armorsmith",
    "Artificer",
    "Chef",
    "Huntsman",
    "Jeweler",
    "Leatherworker",
    "Scribe",
    "Tailor",
    "Weaponsmith",
]

Weapon = Literal[
    "Axe",
    "Dagger",
    "Focus",
    "Greatsword",
    "Hammer",
    "Harpoon",
    "LongBow",
    "Mace",
    "Pistol",
    "Rifle",
    "Scepter",
    "Shield",
    "ShortBow",
    "Speargun",
    "Staff",
    "Sword",
    "Torch",
    "Trident",
    "Warhorn",
    # other "weapons"
    "LargeBundle",
    "SmallBundle",
    "Toy",
    "ToyTwoHanded",
]
WeaponDamage = Literal[
    "Physical",
    "Fire",
    "Lightning",
    "Ice",
    "Choking",
]


SkillSlot = Literal[
    "Downed_1",
    "Downed_2",
    "Downed_3",
    "Downed_4",
    "Pet",
    "Toolbelt",
    "Profession_1",
    "Profession_2",
    "Profession_3",
    "Profession_4",
    "Profession_5",
    "Weapon_1",
    "Weapon_2",
    "Weapon_3",
    "Weapon_4",
    "Weapon_5",
    "Heal",
    "Utility",
    "Elite",
    "Transform_1",
]


ArmorWeight = Literal["Clothing", "Light", "Medium", "Heavy"]
ArmorType = Literal[
    "Boots",
    "Coat",
    "Gloves",
    "Helm",
    "HelmAquatic",
    "Leggings",
    "Shoulders",
]

DyeMaterial = Literal["cloth", "leather", "metal", "fur"]

Region = Literal[
    "Tyria",
    "Maguuma",
    "Desert",
    "Tundra",
    "Unknown",
    "Cantha",
    "Jade",
    "Sky",
]

Attribute = Literal[
    "AgonyResistance",
    "BoonDuration",
    "ConditionDamage",
    "ConditionDuration",
    "CritDamage",
    "Healing",
    "Power",
    "Precision",
    "Toughness",
    "Vitality",
]


class EmptyObject(BaseModel): ...


class DyeSlot(BaseModel):
    color_id: int
    material: DyeMaterial


class PrefixedBuff(BaseModel):
    text: str
    icon: AnyHttpUrl
    status: str | None = None
    description: str | None = None


class Fact(BaseModel):
    # todo: tagged union, somehow...
    text: str | None = None
    icon: AnyHttpUrl | None = None
    type: (
        Literal[
            "AttributeAdjust",
            "Buff",
            "BuffConversion",
            "ComboField",
            "ComboFinisher",
            "Damage",
            "Distance",
            "NoData",
            "Number",
            "Percent",
            "PrefixedBuff",
            "Radius",
            "Range",
            "Recharge",
            "StunBreak",
            "Time",
            "Unblockable",
            "Duration",
            "HealingAdjust",
        ]
        | None
    ) = None
    # AttributeAdjust/Number/Range/Recharge/Unblockable
    value: int | float | None = None
    # AttributeAdjust/BuffConversion
    target: str | None = None
    # Buff/PrefixedBuff
    status: str | None = None
    description: str | None = None
    apply_count: int | None = None
    # Buff/PrefixedBuff/Time
    duration: int | None = None
    # BuffConversion/Percent
    percent: int | float | None = None
    # BuffConversion
    source: str | None = None
    # ComboField
    field_type: (
        Literal[
            "Air",
            "Dark",
            "Fire",
            "Ice",
            "Light",
            "Lightning",
            "Poison",
            "Smoke",
            "Ethereal",
            "Water",
        ]
        | None
    ) = None
    # ComboFinisher
    finisher_type: (
        Literal[
            "Blast",
            "Leap",
            "Projectile",
            "Whirl",
        ]
        | None
    ) = None
    # Damage
    hit_count: int | None = None
    # Distance/Radius
    distance: int | None = None
    # PrefixedBuff
    prefix: PrefixedBuff | None = None
    # ???
    dmg_multiplier: float | None = None
    chance: int | None = None


class TraitedFact(Fact):
    requires_trait: int
    overrides: int | None = None


Binding = Literal["Account", "Character"]


class Stats(BaseModel):
    id: int
    # That's way too annoying to define in a clear way
    attributes: dict[str, int]


class InventorySlot(BaseModel):
    """
    https://wiki.guildwars2.com/wiki/API:2/account/bank
    https://wiki.guildwars2.com/wiki/API:2/characters/inventory
    """

    id: int
    count: int

    binding: Binding | None = None
    bound_to: str | None = None
    charges: int | None = None
    dyes: list[int] | None = None
    infusions: list[int] | None = None
    skin: int | None = None
    stats: Stats | None = None
    upgrade_slot_indices: list[int] | None = None
    upgrades: list[int] | None = None


class BuildTab(BaseModel):
    class Build(BaseModel):
        """
        https://wiki.guildwars2.com/wiki/API:2/account/buildstorage
        https://wiki.guildwars2.com/wiki/API:2/characters/buildtabs
        """

        class Skills(BaseModel):
            heal: int | None = None
            utilities: list[int | None] = []
            elite: int | None = None

        class Specialization(BaseModel):
            id: int | None
            traits: list[int | None] = []

        class Pets(BaseModel):
            terrestrial: list[int | None] = []
            aquatic: list[int | None] = []

        name: str
        profession: Profession
        specializations: list[Specialization] = Field(min_length=3, max_length=3)
        skills: Skills
        aquatic_skills: Skills
        pets: Pets | None = None
        # todo: XXX: this is currently bugged and should be a revenant legend instead
        legends: (
            list[
                Annotated[
                    Literal[
                        "Legend1",
                        "Legend2",
                        "Legend3",
                        "Legend4",
                        "Legend6",
                        "Legend5",
                    ],
                    EnumValidator,
                ]
                | Unknown
                | None
            ]
            | None
        ) = None
        aquatic_legends: list[str | None] | None = None

        # TODO: Actual specialization since that's not in profession (spec ids)

    tab: int  # Tab number
    is_active: bool
    build: Build


def coerce_weapon(val: str) -> str | None:
    """
    Coerce weapon type into proper name
    """
    # todo: replace with aliases, if possible

    if val == "None":
        return None

    # inconsistency: professions, skills, skins use Shortbow instead of ShortBow
    if val == "Shortbow":
        return "ShortBow"
    if val == "Longbow":
        return "LongBow"

    # spears are harpoons
    if val == "Spear":
        return "Harpoon"

    return val
