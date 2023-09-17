from typing import TYPE_CHECKING

from gw2 import models
from gw2.models import account, common

from ._base import Base, IdsBase, ListBase

if TYPE_CHECKING:
    from gw2.api import home


class Account(Base[models.Account], _type=models.Account):
    def achievements(self) -> "Achievements":
        client = Achievements()
        client.auth(self.api_key)
        return client

    def bank(self) -> "Bank":
        client = Bank()
        client.auth(self.api_key)
        return client

    def build_storage(self) -> "BuildStorage":
        client = BuildStorage()
        client.auth(self.api_key)
        return client

    def daily_crafting(self) -> "DailyCrafting":
        client = DailyCrafting()
        client.auth(self.api_key)
        return client

    def dungeons(self) -> "Dungeons":
        client = Dungeons()
        client.auth(self.api_key)
        return client

    def dyes(self) -> "Dyes":
        client = Dyes()
        client.auth(self.api_key)
        return client

    def finishers(self) -> "Finishers":
        client = Finishers()
        client.auth(self.api_key)
        return client

    def gliders(self) -> "Gliders":
        client = Gliders()
        client.auth(self.api_key)
        return client

    def home_cats(self) -> "home.HomeCats":
        from gw2.api.home import HomeCats

        client = HomeCats()
        client.auth(self.api_key)
        return client

    def home_nodes(self) -> "home.HomeNodes":
        from gw2.api.home import HomeNodes

        client = HomeNodes()
        client.auth(self.api_key)
        return client

    def legendary_armory(self) -> "LegendaryArmory":
        client = LegendaryArmory()
        client.auth(self.api_key)
        return client

    def luck(self) -> "Luck":
        client = Luck()
        client.auth(self.api_key)
        return client

    def mail_carriers(self) -> "MailCarriers":
        client = MailCarriers()
        client.auth(self.api_key)
        return client

    def map_chests(self) -> "MapChests":
        client = MapChests()
        client.auth(self.api_key)
        return client

    def masteries(self) -> "Masteries":
        client = Masteries()
        client.auth(self.api_key)
        return client

    def mastery_points(self) -> "MasteryPoints":
        client = MasteryPoints()
        client.auth(self.api_key)
        return client

    def materials(self) -> "Materials":
        client = Materials()
        client.auth(self.api_key)
        return client

    def minis(self) -> "Minis":
        client = Minis()
        client.auth(self.api_key)
        return client

    def mount_skins(self) -> "MountSkins":
        client = MountSkins()
        client.auth(self.api_key)
        return client

    def mount_types(self) -> "MountTypes":
        client = MountTypes()
        client.auth(self.api_key)
        return client

    def novelties(self) -> "Novelties":
        client = Novelties()
        client.auth(self.api_key)
        return client

    def outfits(self) -> "Outfits":
        client = Outfits()
        client.auth(self.api_key)
        return client

    def progression(self) -> "Progression":
        client = Progression()
        client.auth(self.api_key)
        return client

    def pvp_heroes(self) -> "PvPHeroes":
        client = PvPHeroes()
        client.auth(self.api_key)
        return client

    def raids(self) -> "Raids":
        client = Raids()
        client.auth(self.api_key)
        return client

    def recipes(self) -> "Recipes":
        client = Recipes()
        client.auth(self.api_key)
        return client

    def shared_inventory(self) -> "SharedInventory":
        client = SharedInventory()
        client.auth(self.api_key)
        return client

    def skins(self) -> "Skins":
        client = Skins()
        client.auth(self.api_key)
        return client

    def titles(self) -> "Titles":
        client = Titles()
        client.auth(self.api_key)
        return client

    def wallet(self) -> "Wallet":
        client = Wallet()
        client.auth(self.api_key)
        return client

    def world_bosses(self) -> "WorldBosses":
        client = WorldBosses()
        client.auth(self.api_key)
        return client


class Achievements(
    ListBase[account.Achievement],
    _type=account.Achievement,
):
    suffix = "account/achievements"


class Bank(ListBase[common.InventorySlot | None], _type=common.InventorySlot):
    suffix = "account/bank"


class BuildStorage(IdsBase[common.BuildTab.Build, int], _type=common.BuildTab.Build):
    suffix = "account/buildstorage"


class DailyCrafting(ListBase[str], _type=str):
    suffix = "account/dailycrafting"


class Dungeons(ListBase[str], _type=str):
    suffix = "account/dungeons"


class Dyes(ListBase[int], _type=int):
    suffix = "account/dyes"


class Finishers(ListBase[account.Finisher], _type=account.Finisher):
    suffix = "account/finishers"


class Gliders(ListBase[int], _type=int):
    suffix = "account/gliders"


class LegendaryArmory(ListBase[account.LegendaryArmory], _type=account.LegendaryArmory):
    suffix = "account/legendaryarmory"


class Luck(ListBase[account.Luck], _type=account.Luck):
    suffix = "account/luck"


class MailCarriers(ListBase[int], _type=int):
    suffix = "account/mailcarriers"


class MapChests(ListBase[str], _type=str):
    suffix = "account/mapchests"


class Masteries(ListBase[account.Mastery], _type=account.Mastery):
    suffix = "account/masteries"


class MasteryPoints(Base[account.MasteryPoints], _type=account.MasteryPoints):
    suffix = "account/mastery/points"


class Materials(ListBase[account.Material], _type=account.Material):
    suffix = "account/materials"


class Minis(ListBase[int], _type=int):
    suffix = "account/minis"


class MountTypes(ListBase[str], _type=str):
    suffix = "account/mounts/types"


class MountSkins(ListBase[int], _type=int):
    suffix = "account/mounts/skins"


class Novelties(ListBase[int], _type=int):
    suffix = "account/novelties"


class Outfits(ListBase[int], _type=int):
    suffix = "account/outfits"


class Progression(ListBase[account.Progression], _type=account.Progression):
    suffix = "account/progression"


class PvPHeroes(ListBase[int], _type=int):
    suffix = "account/pvp/heroes"


class Raids(ListBase[str], _type=str):
    suffix = "account/raids"


class Recipes(ListBase[int], _type=int):
    suffix = "account/recipes"


class SharedInventory(
    ListBase[account.SharedInventorySlot], _type=account.SharedInventorySlot
):
    suffix = "account/inventory"


class Skins(ListBase[int], _type=int):
    suffix = "account/skins"


class Titles(ListBase[int], _type=int):
    suffix = "account/titles"


class Wallet(ListBase[account.WalletEntry], _type=account.WalletEntry):
    suffix = "account/wallet"


class WorldBosses(ListBase[str], _type=str):
    suffix = "account/worldbosses"
