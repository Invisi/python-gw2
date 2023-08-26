# python-gw2
A Python wrapper for easy and typed access of Guild Wars 2's API.

## Installation
### Requirements
- Python >= 3.10
- httpx
- pydantic

Since this project is currently not released on PyPi, the easiest way of installing it
is as follows:
```bash
# With poetry
$ poetry add git+https://github.com/Invisi/python-gw2.git
# With pip
$ pip install git+https://github.com/Invisi/python-gw2.git#egg=gw2
```

## Basic usage
```python
from gw2.api import Account, Character

async with Account() as client:
    # Authenticates *this instance* for this endpoint
    client.auth("ABCDE-...")
    data = await client.get()

    print(data.commander)  # True
    print(data.last_modified)  # a datetime instance

async with Account() as client:
    # Authenticate for this instance and all following instances
    client.global_auth("ABCDE-...")
    data = await client.get()

    print(data.last_modified)  # still a datetime instance

async with Character("Some Character") as client:
    # Retrieve data with previously set API key
    data = await client.get()

    print(data.profession)  # Profession.ELEMENTALIST

# ...
```

## Supported endpoints
- (The asset CDN for the build id in case the API is down)
<details>
<summary>Big list of endpoints</summary>

- /v2.json
- /v2/account (without detail endpoints)
- /v2/account/achievements
- /v2/achievements
- /v2/achievements/categories
- /v2/achievements/groups
- /v2/build
- /v2/characters (without detail endpoints)
- /v2/colors
- /v2/currencies
- /v2/finishers
- /v2/gliders
- /v2/guild/:id/ (without detail endpoints)
- /v2/guild/upgrades
- /v2/minis
- /v2/novelties
- /v2/outfits
- /v2/pets
- /v2/professions
- /v2/quests
- /v2/recipes
- /v2/skills
- /v2/skins
- /v2/specializations
- /v2/stories
- /v2/stories/seasons
- /v2/titles
- /v2/tokeninfo
- /v2/worlds
- /v2/wvw/matches
- /v2/wvw/matches/overview
</details>


## Planned features
- ID-based caching
- Rate limiting
- The other endpoints I potentially forgot about

<details>
<summary>Another big list of endpoints</summary>

- /v2/account/*
- /v2/achievements/(daily, tomorrow)
- /v2/backstory/*
- /v2/characters/*
- /v2/continents
- /v2/createsubtoken
- /v2/dailycrafting
- /v2/dungeons
- /v2/emblem/(backgrounds, foregrounds)
- /v2/emotes
- /v2/files
- /v2/guild/:id/*
- /v2/guild/(permissions, search)
- /v2/home/(cats, nodes)
- /v2/items
- /v2/itemstats
- /v2/legendaryarmory
- /v2/legends
- /v2/mailcarriers
- /v2/mapchests
- /v2/maps
- /v2/maps
- /v2/masteries
- /v2/materials
- /v2/mounts/(skins, types)
- /v2/pvp/*
- /v2/quaggans
- /v2/races
- /v2/raids
- /v2/recipes/search
- /v2/worldbosses
- /v2/wvw/(abilities,objectives,ranks,upgrades)
</details>


## License
[MIT](LICENSE)
