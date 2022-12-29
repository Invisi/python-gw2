# python-gw2
A Python wrapper for easy and typed access of Guild Wars 2's API.

## Installation
### Requirements
- Python >= 3.8
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
- /v2/account
- /v2/account/achievements
- /v2/build
- /v2/characters (without detail endpoints)
- /v2/guild
- /v2/tokeninfo
- (The asset CDN for the build id in case the API is down)

## Planned features
- ID-based caching
- The other endpoints

## License
[MIT](LICENSE)
