import httpx

from gw2 import models
from gw2.api._base import Base


class Build(Base[models.Build], _type=models.Build):
    pass


class BuildManifest:
    @staticmethod
    async def get() -> models.BuildManifest:
        """
        Retrieves the build ID (and some additional information) from the asset
        CDN.
        Can be used as an alternative way in case the main API's ID gets stuck.

        Raises:
             httpx.HTTPStatusError
             ValueError
        """
        async with httpx.AsyncClient() as ac:
            response = await ac.get(
                "http://assetcdn.101.arenanetworks.com/latest64/101"
            )

            data = response.text.split(" ")
            return models.BuildManifest(*[int(_) for _ in data])
