import gw2
from gw2 import models
from gw2.models import common


def test_klass() -> None:
    assert gw2.Account()._klass == models.Account

    assert gw2.Masteries()._klass == list[models.Mastery]
    assert gw2.Mastery(1)._klass == models.Mastery

    assert gw2.Achievements()._klass == list[models.Achievement]

    assert gw2.Dungeons()._klass == list[models.Dungeon]
    assert gw2.Account().daily_crafting()._klass == list[str]
    assert gw2.Account().bank()._klass == list[common.InventorySlot | None]
