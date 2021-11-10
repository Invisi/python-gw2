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
from gw2.api import Account

client = Account()

# Authenticates globally for all endpoints
client.auth("ABCDE-...")

data = await client.get()
print(data.commander)  # True
print(data.last_modified)  # a datetime instance
# ...
```

## Supported endpoints
- /v2/account
- /v2/account/achievements
- /v2/build
- (The asset CDN for the build id in case the API is down)

## Planned features
- ID-based caching
- The other endpoints

## License
[MIT](LICENSE)