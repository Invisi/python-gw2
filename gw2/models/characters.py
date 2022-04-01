import datetime
import enum
import uuid
from typing import Dict, List, Literal, Optional

from pydantic import conlist

from gw2.models._base import BaseModel

# TODO: Replace enums with literals
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


class EquipmentSlot(enum.Enum):
    ACCESSORY1 = "Accessory1"
    ACCESSORY2 = "Accessory2"
    AMULET = "Amulet"
    AXE = "Axe"
    BACKPACK = "Backpack"
    BOOTS = "Boots"
    COAT = "Coat"
    GLOVES = "Gloves"
    HELM = "Helm"
    HELMAQUATIC = "HelmAquatic"
    LEGGINGS = "Leggings"
    PICK = "Pick"
    RING1 = "Ring1"
    RING2 = "Ring2"
    SHOULDERS = "Shoulders"
    SICKLE = "Sickle"
    WEAPONA1 = "WeaponA1"
    WEAPONA2 = "WeaponA2"
    WEAPONAQUATICA = "WeaponAquaticA"
    WEAPONAQUATICB = "WeaponAquaticB"
    WEAPONB1 = "WeaponB1"
    WEAPONB2 = "WeaponB2"


Gender = Literal["Female", "Male"]
Binding = Literal["Account", "Character"]


class Location(enum.Enum):
    EQUIPPED = "Equipped"
    ARMORY = "Armory"
    EQUIPPED_FROM_LEGENDARY_ARMORY = "EquippedFromLegendaryArmory"
    LEGENDARY_ARMORY = "LegendaryArmory"


# --- Enums above, scary things below


class Crafting(BaseModel):
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

    discipline: Discipline
    rating: int
    active: bool


class WvWAbility(BaseModel):
    id: int
    rank: int


class BuildTab(BaseModel):
    class Build(BaseModel):
        class Skills(BaseModel):
            heal: Optional[int]
            utilities: conlist(item_type=Optional[int], min_items=3, max_items=3)
            elite: Optional[int]

        class Specialization(BaseModel):
            id: Optional[int]
            traits: conlist(item_type=Optional[int], min_items=3, max_items=3)

        name: str
        profession: Profession
        specializations: conlist(item_type=Specialization, min_items=3, max_items=3)
        skills: Skills
        aquatic_skills: Skills

        # TODO: Actual specialization since that's not in profession (spec ids)

    tab: int  # Tab number
    is_active: bool
    build: Build


class Stats(BaseModel):
    id: int
    # That's way too annoying to define in a clear way
    attributes: Dict[str, int]


class Equipment(BaseModel):
    id: int
    slot: Optional[EquipmentSlot] = None

    infusions: Optional[List[int]] = None
    upgrades: Optional[List[int]] = None
    skin: Optional[int] = None
    stats: Optional[Stats] = None
    binding: Optional[Binding] = None
    location: Location
    tabs: Optional[List[int]] = None
    charges: Optional[int] = None
    bound_to: Optional[str] = None
    dyes: Optional[List[Optional[int]]] = None


class EquipmentPvP(BaseModel):
    amulet: Optional[int]
    rune: Optional[int]
    sigils: conlist(item_type=Optional[int], min_items=4, max_items=4)


class EquipmentTabs(BaseModel):
    tab: int
    name: str
    is_active: bool
    equipment: List[Equipment]
    equipment_pvp: EquipmentPvP


class Training(BaseModel):
    id: int
    spent: int
    done: bool


class InventorySlot(BaseModel):
    id: int
    count: int
    charges: Optional[int] = None
    infusions: Optional[List[int]] = None
    upgrades: Optional[List[int]] = None
    skin: Optional[int] = None
    stats: Optional[Stats] = None
    binding: Optional[Binding] = None
    bound_to: Optional[str] = None


class Bag(BaseModel):
    id: int
    size: int
    inventory: List[Optional[InventorySlot]]


class Character(BaseModel):
    name: str
    race: Race
    gender: Gender
    flags: List[str]
    profession: Profession
    level: int
    guild: Optional[uuid.UUID]
    age: int

    deaths: int
    crafting: List[Crafting]
    title: Optional[int]
    backstory: List[str]

    last_modified: datetime.datetime
    created: datetime.datetime

    wvw_abilities: List[WvWAbility]
    build_tabs_unlocked: int
    active_build_tab: int
    build_tabs: List[BuildTab]

    active_equipment_tab: int
    equipment: List[Equipment]
    equipment_tabs: List[EquipmentTabs]
    equipment_tabs_unlocked: int

    recipes: List[int]

    training: List[Training]
    bags: List[Optional[Bag]]

    # TODO: Simplified access to inventory


# -- separate endpoints
class CharacterBackstory(BaseModel):
    backstory: List[str]


class CharacterCore(BaseModel):
    name: str
    race: Race
    gender: Gender
    profession: Profession
    level: int
    guild: Optional[uuid.UUID]
    age: int
    deaths: int
    title: Optional[int]

    created: datetime.datetime
    last_modified: datetime.datetime


class CharacterCrafting(BaseModel):
    crafting: List[Crafting]


class CharacterEquipment(BaseModel):
    equipment: List[Equipment]


class CharacterBuildTab(BuildTab):
    pass
