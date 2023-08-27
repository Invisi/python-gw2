"""
Some very very very basic tests to ensure our types still align.
"""
import os

import pytest

import gw2

EFFICIENCY_API_KEY = (
    "564F181A-F0FC-114A-A55D-3C1DCD45F3767AF3848F-AB29-4EBF-9594-F91E6A75E015"
)


@pytest.mark.asyncio
async def test_account() -> None:
    async with gw2.Account() as client:
        client.auth(os.environ.get("API_KEY", EFFICIENCY_API_KEY))
        account = await client.get()

    assert account is not None

    async with gw2.Account().achievements() as client:
        client.auth(os.environ.get("API_KEY", EFFICIENCY_API_KEY))
        account_achievements = await client.get()

    assert account_achievements is not None


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
    characters_client.auth(os.environ.get("API_KEY", EFFICIENCY_API_KEY))
    characters = await characters_client.all_noniter(concurrent=True)

    char_client = gw2.Character(characters[0].name)
    char_client.auth(os.environ.get("API_KEY", EFFICIENCY_API_KEY))
    character = await char_client.get()

    assert character is not None

    backstory = await char_client.backstory().get()
    core = await char_client.core().get()
    crafting = await char_client.crafting().get()
    equipment = await char_client.equipment().get()
    hero_points = await char_client.hero_points().get()
    build_tabs = await char_client.build_tabs().all_noniter(concurrent=True)

    assert backstory is not None
    assert core is not None
    assert crafting is not None
    assert equipment is not None
    assert hero_points is not None
    assert build_tabs is not None


@pytest.mark.asyncio
async def test_colors() -> None:
    many = await gw2.Colors().all_noniter(concurrent=True)
    one = await gw2.Color(many[0].id).get()

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
async def test_guild() -> None:
    guild_id = "14762DCE-C2A4-E711-80D5-441EA14F1E44"
    one = await gw2.Guild(guild_id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_guild_upgrades() -> None:
    many = await gw2.GuildUpgrades().all_noniter(concurrent=True)
    one = await gw2.GuildUpgrade(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_minis() -> None:
    many = await gw2.Minis().all_noniter(concurrent=True)
    one = await gw2.Mini(many[0].id).get()

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
async def test_quests() -> None:
    many = await gw2.Quests().all_noniter(concurrent=True)
    one = await gw2.Quest(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_recipes() -> None:
    many = await gw2.Recipes().all_noniter(concurrent=True)
    one = await gw2.Recipe(many[0].id).get()

    assert one is not None


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
        client.auth(os.environ.get("API_KEY", EFFICIENCY_API_KEY))
        one = client.get()

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
async def test_wvw_matches() -> None:
    many = await gw2.Matches().all_noniter(concurrent=True)
    one = await gw2.Match(many[0].id).get()

    assert one is not None


@pytest.mark.asyncio
async def test_wvw_match_overviews() -> None:
    many = await gw2.MatchOverviews().all_noniter(concurrent=True)
    one = await gw2.MatchOverview(many[0].id).get()

    assert one is not None
