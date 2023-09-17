import functools

from gw2 import models

from ._base import Base, IdsBase


class Continents(IdsBase[models.Continent, int]):
    pass


class Continent(Base[models.Continent]):
    def __init__(self, continent_id: int):
        self.continent_id = continent_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"continents/{self.continent_id}"

    def floors(self) -> "Floors":
        return Floors(self.continent_id)

    def floor(self, floor_id: int) -> "Floor":
        return Floor(self.continent_id, floor_id)


class Floors(IdsBase[models.Floor, int]):
    def __init__(self, continent_id: int):
        self.continent_id = continent_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"continents/{self.continent_id}/floors"


class Floor(Base[models.Floor]):
    def __init__(self, continent_id: int, floor_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"continents/{self.continent_id}/floors/{self.floor_id}"

    def regions(self) -> "Regions":
        return Regions(self.continent_id, self.floor_id)

    def region(self, region_id: int) -> "Region":
        return Region(self.continent_id, self.floor_id, region_id)


class Regions(IdsBase[models.Region, int]):
    def __init__(self, continent_id: int, floor_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"continents/{self.continent_id}/floors/{self.floor_id}/regions"


class Region(Base[models.Region]):
    def __init__(self, continent_id: int, floor_id: int, region_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/"
            f"regions/{self.region_id}"
        )

    def maps(self) -> "ContinentMaps":
        return ContinentMaps(self.continent_id, self.floor_id, self.region_id)

    def map(self, map_id: int) -> "ContinentMap":
        return ContinentMap(self.continent_id, self.floor_id, self.region_id, map_id)


class ContinentMaps(IdsBase[models.ContinentMap, int]):
    def __init__(self, continent_id: int, floor_id: int, region_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps"
        )


class ContinentMap(Base[models.ContinentMap]):
    def __init__(self, continent_id: int, floor_id: int, region_id: int, map_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}"
        )

    def sectors(self) -> "Sectors":
        return Sectors(self.continent_id, self.floor_id, self.region_id, self.map_id)

    def sector(self, sector_id: int) -> "Sector":
        return Sector(
            self.continent_id, self.floor_id, self.region_id, self.map_id, sector_id
        )

    def pois(self) -> "PointsOfInterest":
        return PointsOfInterest(
            self.continent_id, self.floor_id, self.region_id, self.map_id
        )

    def poi(self, poi_id: int) -> "PointOfInterest":
        return PointOfInterest(
            self.continent_id, self.floor_id, self.region_id, self.map_id, poi_id
        )

    def tasks(self) -> "Tasks":
        return Tasks(self.continent_id, self.floor_id, self.region_id, self.map_id)

    def task(self, task_id: int) -> "Task":
        return Task(
            self.continent_id, self.floor_id, self.region_id, self.map_id, task_id
        )


class Sectors(IdsBase[models.Sector, int]):
    def __init__(self, continent_id: int, floor_id: int, region_id: int, map_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/sectors"
        )


class Sector(Base[models.Sector]):
    def __init__(  # noqa: PLR0913
        self,
        continent_id: int,
        floor_id: int,
        region_id: int,
        map_id: int,
        sector_id: int,
    ):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        self.sector_id = sector_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/sectors/{self.sector_id}"
        )


class PointsOfInterest(
    IdsBase[models.PointOfInterest, int],
):
    def __init__(self, continent_id: int, floor_id: int, region_id: int, map_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/pois"
        )


class PointOfInterest(Base[models.PointOfInterest]):
    def __init__(  # noqa: PLR0913
        self, continent_id: int, floor_id: int, region_id: int, map_id: int, poi_id: int
    ):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        self.poi_id = poi_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/pois/{self.poi_id}"
        )


class Tasks(IdsBase[models.Task, int]):
    def __init__(self, continent_id: int, floor_id: int, region_id: int, map_id: int):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/tasks"
        )


class Task(Base[models.Task]):
    def __init__(  # noqa: PLR0913
        self,
        continent_id: int,
        floor_id: int,
        region_id: int,
        map_id: int,
        task_id: int,
    ):
        self.continent_id = continent_id
        self.floor_id = floor_id
        self.region_id = region_id
        self.map_id = map_id
        self.task_id = task_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return (
            f"continents/{self.continent_id}/floors/{self.floor_id}/regions/"
            f"{self.region_id}/maps/{self.map_id}/tasks/{self.task_id}"
        )
