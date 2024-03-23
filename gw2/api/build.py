import httpx

from gw2 import models

from ._base import Base


class Build(Base[models.Build]):
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
            # noinspection HttpUrlsUsage
            response = await ac.get(
                "http://assetcdn.101.arenanetworks.com/latest64/101",
            )

            try:
                data = response.text.split(" ")
                return models.BuildManifest(
                    build_id=data[0],  # type: ignore[arg-type]
                    exe_id=data[1],  # type: ignore[arg-type]
                    exe_size=data[2],  # type: ignore[arg-type]
                    manifest_id=data[3],  # type: ignore[arg-type]
                    manifest_size=data[4],  # type: ignore[arg-type]
                )
            except IndexError as e:
                raise ValueError from e
