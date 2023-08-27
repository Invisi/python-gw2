import enum

from pydantic import AnyHttpUrl

from ._base import BaseModel


class Race(enum.Enum):
    ASURA = "Asura"
    CHARR = "Charr"
    HUMAN = "Human"
    NORN = "Norn"
    SYLVARI = "Sylvari"


class Profession(enum.Enum):
    ELEMENTALIST = "Elementalist"
    ENGINEER = "Engineer"
    GUARDIAN = "Guardian"
    MESMER = "Mesmer"
    NECROMANCER = "Necromancer"
    RANGER = "Ranger"
    REVENANT = "Revenant"
    THIEF = "Thief"
    WARRIOR = "Warrior"


class Discipline(enum.Enum):
    ARMORSMITH = "Armorsmith"
    ARTIFICIER = "Artificer"
    CHEF = "Chef"
    HUNTSMAN = "Huntsman"
    JEWELER = "Jeweler"
    LEATHERWORKER = "Leatherworker"
    SCRIBE = "Scribe"
    TAILOR = "Tailor"
    WEAPONSMITH = "Weaponsmith"


class Weapon(enum.Enum):
    AXE = "Axe"
    DAGGER = "Dagger"
    FOCUS = "Focus"
    GREATSWORD = "Greatsword"
    HAMMER = "Hammer"
    HARPOON = "Harpoon"
    LONGBOW = "LongBow"
    MACE = "Mace"
    PISTOL = "Pistol"
    RIFLE = "Rifle"
    SCEPTER = "Scepter"
    SHIELD = "Shield"
    SHORTBOW = "ShortBow"
    SPEARGUN = "Speargun"
    STAFF = "Staff"
    SWORD = "Sword"
    TORCH = "Torch"
    TRIDENT = "Trident"
    WARHORN = "Warhorn"
    #
    LARGE_BUNDLE = "LargeBundle"
    SMALL_BUNDLE = "SmallBundle"
    TOY = "Toy"
    TOY_TWO_HANDED = "ToyTwoHanded"


class SkillSlot(enum.Enum):
    DOWNED_1 = "Downed_1"
    DOWNED_2 = "Downed_2"
    DOWNED_3 = "Downed_3"
    DOWNED_4 = "Downed_4"
    PET = "Pet"
    TOOLBELT = "Toolbelt"
    PROFESSION_1 = "Profession_1"
    PROFESSION_2 = "Profession_2"
    PROFESSION_3 = "Profession_3"
    PROFESSION_4 = "Profession_4"
    PROFESSION_5 = "Profession_5"
    WEAPON_1 = "Weapon_1"
    WEAPON_2 = "Weapon_2"
    WEAPON_3 = "Weapon_3"
    WEAPON_4 = "Weapon_4"
    WEAPON_5 = "Weapon_5"
    HEAL = "Heal"
    UTILITY = "Utility"
    ELITE = "Elite"


class ArmorWeight(enum.Enum):
    CLOTHING = "Clothing"
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"


class ArmorType(enum.Enum):
    BOOTS = "Boots"
    COAT = "Coat"
    GLOVES = "Gloves"
    HELM = "Helm"
    HELM_AQUATIC = "HelmAquatic"
    LEGGINGS = "Leggings"
    SHOULDERS = "Shoulders"


class FactType(enum.Enum):
    ATTRIBUTE_ADJUST = "AttributeAdjust"
    BUFF = "Buff"
    BUFF_CONVERSION = "BuffConversion"
    COMBO_FIELD = "ComboField"
    COMBO_FINISHER = "ComboFinisher"
    DAMAGE = "Damage"
    DISTANCE = "Distance"
    NODATA = "NoData"
    NUMBER = "Number"
    PERCENT = "Percent"
    PREFIXED_BUFF = "PrefixedBuff"
    RADIUS = "Radius"
    RANGE = "Range"
    RECHARGE = "Recharge"
    STUN_BREAK = "StunBreak"
    TIME = "Time"
    UNBLOCKABLE = "Unblockable"


class ComboFieldType(enum.Enum):
    AIR = "Air"
    DARK = "Dark"
    FIRE = "Fire"
    ICE = "Ice"
    LIGHT = "Light"
    LIGHTNING = "Lightning"
    POISON = "Poison"
    SMOKE = "Smoke"
    ETHEREAL = "Ethereal"
    WATER = "Water"


class ComboFinisherType(enum.Enum):
    BLAST = "Blast"
    LEAP = "Leap"
    PROJECTILE = "Projectile"
    WHIRL = "Whirl"


class PrefixedBuff(BaseModel):
    text: str
    icon: AnyHttpUrl
    status: str | None = None
    description: str | None = None


class Fact(BaseModel):
    text: str | None = None
    icon: AnyHttpUrl | None = None
    type: FactType | None = None
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
    field_type: ComboFieldType | None = None
    # ComboFinisher
    finisher_type: ComboFinisherType | None = None
    # Damage
    hit_count: int | None = None
    # Distance/Radius
    distance: int | None = None
    # PrefixedBuff
    prefix: PrefixedBuff | None = None


class TraitedFact(BaseModel):
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
