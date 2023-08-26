from gw2 import models

from ._base import BASE_URL, Base


class V2(Base[models.V2], _type=models.V2):
    url = f"{BASE_URL}.json"
