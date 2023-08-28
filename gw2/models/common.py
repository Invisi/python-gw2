from typing import Literal

from pydantic import AnyHttpUrl

from ._base import BaseModel

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
    #
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
]


ArmorWeight = Literal["Clothing", "Light", "Medium", "Heavy"]
ArmorType = Literal[
    "Boots", "Coat", "Gloves", "Helm", "HelmAquatic", "Leggings", "Shoulders"
]

DyeMaterial = Literal["cloth", "leather", "metal", "fur"]


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
    type: Literal[
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
    ] | None = None
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
    field_type: Literal[
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
    ] | None = None
    # ComboFinisher
    finisher_type: Literal[
        "Blast",
        "Leap",
        "Projectile",
        "Whirl",
    ] | None = None
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
