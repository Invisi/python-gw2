import os

import pytest

from gw2 import gw2treasures, models

GW2TREASURES_API_KEY = os.environ.get("GW2TREASURES_API_KEY")


@pytest.mark.asyncio
async def test_achievements() -> None:
    if GW2TREASURES_API_KEY is None:
        raise Exception("GW2TREASURES_API_KEY environment variable is not set")

    achievement = None
    async for achievement in gw2treasures.Achievements(GW2TREASURES_API_KEY).many(
        [2789, 1, 2, 3, 4, 5, 6],
    ):
        assert isinstance(achievement, models.Achievement)

    one = await gw2treasures.Achievement(GW2TREASURES_API_KEY, achievement.id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_items() -> None:
    if GW2TREASURES_API_KEY is None:
        raise Exception("GW2TREASURES_API_KEY environment variable is not set")

    item = None
    async for item in gw2treasures.Items(GW2TREASURES_API_KEY).many(
        [39119, 39120, 39121, 39122, 39123, 39123, 39124],
    ):
        assert isinstance(item, models.Item)

    one = await gw2treasures.Item(GW2TREASURES_API_KEY, item.id).get()

    assert one is not None
