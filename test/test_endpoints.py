"""
Some very very very basic tests to ensure our types still align.
"""
import os

import pytest

import gw2
from gw2 import errors, models

API_KEY = os.environ.get(
    "API_KEY",
    "564F181A-F0FC-114A-A55D-3C1DCD45F3767AF3848F-AB29-4EBF-9594-F91E6A75E015",
)
GUILD_ID = os.environ.get("GUILD_ID", "14762DCE-C2A4-E711-80D5-441EA14F1E44")


@pytest.fixture(scope="function")
def account() -> gw2.Account:
    client = gw2.Account()
    client.auth(API_KEY)
    return client


@pytest.fixture
def guild() -> gw2.Guild:
    client = gw2.Guild(GUILD_ID)
    client.auth(API_KEY)
    return client


@pytest.mark.asyncio
async def test_account(account: gw2.Account) -> None:
    data = await account.get()

    assert data is not None


@pytest.mark.parametrize(
    "fn",
    [
        "achievements",
        "bank",
        "build_storage",
        "daily_crafting",
        "dungeons",
        "dyes",
        "finishers",
        "gliders",
        "home_cats",
        "home_nodes",
        "legendary_armory",
        "luck",
        "mail_carriers",
        "map_chests",
        "masteries",
        "mastery_points",
        "materials",
        "minis",
        "mount_skins",
        "mount_types",
        "novelties",
        "outfits",
        "progression",
        "pvp_heroes",
        "raids",
        "recipes",
        "shared_inventory",
        "skins",
        "titles",
        "wallet",
        "world_bosses",
    ],
)
@pytest.mark.asyncio
async def test_account_endpoint(account: gw2.Account, fn: str) -> None:
    async with getattr(account, fn)() as sub_client:
        if hasattr(sub_client, "all_noniter"):
            assert await sub_client.all_noniter(concurrent=True) is not None
        if hasattr(sub_client, "get"):
            assert await sub_client.get() is not None
        if hasattr(sub_client, "ids"):
            assert await sub_client.ids() is not None


@pytest.mark.asyncio
async def test_achievements() -> None:
    many = await gw2.Achievements().all_noniter(concurrent=True)
    one = await gw2.Achievement(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_achievement_categories() -> None:
    many = await gw2.AchievementCategories().all_noniter(concurrent=True)
    one = await gw2.AchievementCategory(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_achievement_groups() -> None:
    many = await gw2.AchievementGroups().all_noniter(concurrent=True)
    one = await gw2.AchievementGroup(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_backstory_questions() -> None:
    many = await gw2.BackstoryQuestions().all_noniter(concurrent=True)
    one = await gw2.BackstoryQuestion(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_backstory_answers() -> None:
    many = await gw2.BackstoryAnswers().all_noniter(concurrent=True)
    one = await gw2.BackstoryAnswer(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_build() -> None:
    build = await gw2.Build().get()
    build_manifest = await gw2.BuildManifest().get()

    assert build is not None
    assert build_manifest is not None


@pytest.mark.asyncio
async def test_characters() -> None:
    characters_client = gw2.Characters()
    characters_client.auth(API_KEY)
    characters = await characters_client.all_noniter(concurrent=True)

    char_client = gw2.Character(characters[0].name)
    char_client.auth(API_KEY)
    character = await char_client.get()

    assert character is not None

    backstory = await char_client.backstory().get()
    build_tabs = await char_client.build_tabs().all_noniter(concurrent=True)
    core = await char_client.core().get()
    crafting = await char_client.crafting().get()
    equipment = await char_client.equipment().get()
    equipment_tabs = await char_client.equipment_tabs().all_noniter(concurrent=True)
    inventory = await char_client.inventory().get()
    quests = await char_client.quests().get()
    recipes = await char_client.recipes().get()
    sab = await char_client.sab().get()

    assert backstory is not None
    assert build_tabs is not None
    assert core is not None
    assert crafting is not None
    assert equipment is not None
    assert equipment_tabs is not None
    assert inventory is not None
    assert quests is not None
    assert recipes is not None
    assert sab is not None


@pytest.mark.asyncio
async def test_colors() -> None:
    many = await gw2.Colors().all_noniter(concurrent=True)
    one = await gw2.Color(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continents() -> None:
    many = await gw2.Continents().all_noniter(concurrent=True)
    one = await gw2.Continent(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floors() -> None:
    continent_id = 1

    many = await gw2.Floors(continent_id).all_noniter(concurrent=True)
    one = await gw2.Floor(continent_id, many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floor_regions() -> None:
    continent_id = 1
    floor_id = 1

    many = await gw2.Regions(continent_id, floor_id).all_noniter(concurrent=True)
    one = await gw2.Region(continent_id, floor_id, many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floor_region_maps() -> None:
    continent_id = 1
    floor_id = 1
    region_id = 1

    many = await gw2.ContinentMaps(continent_id, floor_id, region_id).all_noniter(
        concurrent=True
    )
    one = await gw2.ContinentMap(continent_id, floor_id, region_id, many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floor_region_map_sectors() -> None:
    continent_id = 1
    floor_id = 1
    region_id = 1
    map_id = 26

    many = await gw2.Sectors(continent_id, floor_id, region_id, map_id).all_noniter(
        concurrent=True
    )
    one = await gw2.Sector(continent_id, floor_id, region_id, map_id, many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floor_region_map_pois() -> None:
    continent_id = 1
    floor_id = 1
    region_id = 1
    map_id = 26

    many = await gw2.PointsOfInterest(
        continent_id, floor_id, region_id, map_id
    ).all_noniter(concurrent=True)
    one = await gw2.PointOfInterest(
        continent_id, floor_id, region_id, map_id, many[0].id
    ).get()

    assert one is not None


@pytest.mark.asyncio
async def test_continent_floor_region_tasks() -> None:
    continent_id = 1
    floor_id = 1
    region_id = 1
    map_id = 26

    many = await gw2.Tasks(continent_id, floor_id, region_id, map_id).all_noniter(
        concurrent=True
    )
    one = await gw2.Task(continent_id, floor_id, region_id, map_id, many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_currencies() -> None:
    many = await gw2.Currencies().all_noniter(concurrent=True)
    one = await gw2.Currency(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_daily_crafting() -> None:
    many = await gw2.DailyCrafting().get()
    assert many is not None


@pytest.mark.asyncio
async def test_dungeons() -> None:
    many = await gw2.Dungeons().get()
    one = await gw2.Dungeon(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_emblem_backgrounds() -> None:
    many = await gw2.EmblemBackgrounds().all_noniter(concurrent=True)
    one = await gw2.EmblemBackground(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_emblem_foregrounds() -> None:
    many = await gw2.EmblemForegrounds().all_noniter(concurrent=True)
    one = await gw2.EmblemForeground(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_emotes() -> None:
    many = await gw2.Emotes().all_noniter(concurrent=True)
    one = await gw2.Emote(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_api_details() -> None:
    one = await gw2.V2().get()
    assert one is not None


@pytest.mark.asyncio
async def test_files() -> None:
    many = await gw2.Files().all_noniter()
    one = await gw2.File(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_finishers() -> None:
    many = await gw2.Finishers().all_noniter(concurrent=True)
    one = await gw2.Finisher(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_gliders() -> None:
    many = await gw2.Gliders().all_noniter(concurrent=True)
    one = await gw2.Glider(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_guild(guild: gw2.Guild) -> None:
    auth_guild = await guild.get()
    normal_guild = await gw2.Guild("4BBB52AA-D768-4FC6-8EDE-C299F2822F0F").get()

    assert isinstance(auth_guild, models.AuthenticatedGuild)
    assert isinstance(normal_guild, models.Guild)


@pytest.mark.asyncio
async def test_guild_search() -> None:
    ids_list = await gw2.GuildSearch("ArenaNet").ids()
    guild = await gw2.GuildSearch("ArenaNet").get()

    assert len(ids_list) > 0 and ids_list[0] == "4BBB52AA-D768-4FC6-8EDE-C299F2822F0F"
    assert guild.id == "4BBB52AA-D768-4FC6-8EDE-C299F2822F0F"

    with pytest.raises(errors.GuildNotFoundError):
        await gw2.GuildSearch("_______").get()


@pytest.mark.asyncio
async def test_guild_log(guild: gw2.Guild) -> None:
    one = await guild.log().get()

    assert one is not None


@pytest.mark.parametrize(
    "fn",
    ["log", "members", "ranks", "stash", "storage", "teams", "treasury", "upgrades"],
)
@pytest.mark.asyncio
async def test_guild_endpoint(guild: gw2.Guild, fn: str) -> None:
    async with getattr(guild, fn)() as sub_client:
        if hasattr(sub_client, "all_noniter"):
            assert await sub_client.all_noniter(concurrent=True) is not None
        if hasattr(sub_client, "get"):
            assert await sub_client.get() is not None
        if hasattr(sub_client, "ids"):
            assert await sub_client.ids() is not None


@pytest.mark.asyncio
async def test_guild_permissions() -> None:
    many = await gw2.GuildPermissions().get()
    one = await gw2.GuildPermission(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_guild_upgrades() -> None:
    many = await gw2.GuildUpgrades().all_noniter(concurrent=True)
    one = await gw2.GuildUpgrade(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_home_cats() -> None:
    many = await gw2.HomeCats().all_noniter(concurrent=True)
    one = await gw2.HomeCat(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_home_nodes() -> None:
    many = await gw2.HomeNodes().get()
    one = await gw2.HomeNode(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_items() -> None:
    many = await gw2.Items().all_noniter(concurrent=True)
    one = await gw2.Item(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_item_stats() -> None:
    many = await gw2.ItemStats().all_noniter(concurrent=True)
    one = await gw2.ItemStat(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_legendary_armory() -> None:
    many = await gw2.LegendaryArmory().all_noniter(concurrent=True)
    one = await gw2.LegendaryArmoryItem(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_legends() -> None:
    many = await gw2.Legends().all_noniter(concurrent=True)
    one = await gw2.Legend(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_mail_carriers() -> None:
    many = await gw2.MailCarriers().all_noniter(concurrent=True)
    one = await gw2.MailCarrier(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_map_chests() -> None:
    many = await gw2.MapChests().all_noniter(concurrent=True)
    one = await gw2.MapChest(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_maps() -> None:
    many = await gw2.Maps().all_noniter(concurrent=True)
    one = await gw2.Map(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_masteries() -> None:
    many = await gw2.Masteries().all_noniter(concurrent=True)
    one = await gw2.Mastery(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_materials() -> None:
    many = await gw2.Materials().all_noniter(concurrent=True)
    one = await gw2.Material(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_minis() -> None:
    many = await gw2.Minis().all_noniter(concurrent=True)
    one = await gw2.Mini(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_mount_skins() -> None:
    many = await gw2.MountSkins().all_noniter(concurrent=True)
    one = await gw2.MountSkin(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_mount_types() -> None:
    many = await gw2.MountTypes().get()
    one = await gw2.MountType(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_novelties() -> None:
    many = await gw2.Novelties().all_noniter(concurrent=True)
    one = await gw2.Novelty(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_outfits() -> None:
    many = await gw2.Outfits().all_noniter(concurrent=True)
    one = await gw2.Outfit(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_pets() -> None:
    many = await gw2.Pets().all_noniter(concurrent=True)
    one = await gw2.Pet(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_professions() -> None:
    many = await gw2.Professions().all_noniter(concurrent=True)
    one = await gw2.Profession(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_quaggans() -> None:
    many = await gw2.Quaggans().get()
    one = await gw2.Quaggan(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_quests() -> None:
    many = await gw2.Quests().all_noniter(concurrent=True)
    one = await gw2.Quest(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_races() -> None:
    many = await gw2.Races().get()
    one = await gw2.Race(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_raids() -> None:
    many = await gw2.Raids().all_noniter(concurrent=True)
    one = await gw2.Raid(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_recipes() -> None:
    many = await gw2.Recipes().all_noniter(concurrent=True)
    one = await gw2.Recipe(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_recipe_search() -> None:
    many = await gw2.RecipeSearch(input_id=48805).all_noniter(concurrent=True)
    more = await gw2.RecipeSearch(output_id=95400).all_noniter(concurrent=True)
    lots = await gw2.Recipes.search(output_id=95400).all_noniter(concurrent=True)

    assert len(many) > 0
    assert len(more) > 0
    assert len(lots) > 0


@pytest.mark.asyncio
async def test_skills() -> None:
    many = await gw2.Skills().all_noniter(concurrent=True)
    one = await gw2.Skill(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_skins() -> None:
    many = await gw2.Skins().all_noniter(concurrent=True)
    one = await gw2.Skin(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_specializations() -> None:
    many = await gw2.Specializations().all_noniter(concurrent=True)
    one = await gw2.Specialization(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_stories() -> None:
    many = await gw2.Stories().all_noniter(concurrent=True)
    one = await gw2.Story(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_story_seasons() -> None:
    many = await gw2.StorySeasons().all_noniter(concurrent=True)
    one = await gw2.StorySeason(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_titles() -> None:
    many = await gw2.Titles().all_noniter(concurrent=True)
    one = await gw2.Title(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_tokeninfo() -> None:
    async with gw2.TokenInfo() as client:
        client.auth(API_KEY)
        one = await client.get()

    assert one is not None


@pytest.mark.asyncio
async def test_traits() -> None:
    many = await gw2.Traits().all_noniter(concurrent=True)
    one = await gw2.Trait(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_worlds() -> None:
    many = await gw2.Worlds().all_noniter(concurrent=True)
    one = await gw2.World(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_worldbosses() -> None:
    many = await gw2.WorldBosses().get()
    one = await gw2.WorldBoss(many[0]).get()

    assert one is not None


@pytest.mark.asyncio
async def test_wvw_matches() -> None:
    many = await gw2.Matches().all_noniter(concurrent=True)
    one = await gw2.Match(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_wvw_match_overviews() -> None:
    many = await gw2.MatchOverviews().all_noniter(concurrent=True)
    one = await gw2.MatchOverview(many[0].id).get()

    assert one is not None
