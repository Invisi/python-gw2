import functools
from typing import cast, overload

from gw2 import models

from ._base import Base, IdsBase


class Recipes(IdsBase[models.Recipe, int]):
    @staticmethod
    @overload
    def search(*, input_id: int) -> "RecipeSearch": ...

    @staticmethod
    @overload
    def search(*, output_id: int) -> "RecipeSearch": ...

    @staticmethod
    def search(
        *, input_id: int | None = None, output_id: int | None = None
    ) -> "RecipeSearch":
        if input_id:
            return RecipeSearch(input_id=input_id)
        else:
            return RecipeSearch(output_id=cast(int, output_id))


class Recipe(Base[models.Recipe]):
    def __init__(self, recipe_id: int):
        self.recipe_id = recipe_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"recipes/{self.recipe_id}"


class RecipeSearch(IdsBase[models.Recipe, int]):
    suffix = "recipes/search"

    @overload
    def __init__(self, *, input_id: int): ...

    @overload
    def __init__(self, *, output_id: int): ...

    def __init__(self, *, input_id: int | None = None, output_id: int | None = None):
        self.input_id = input_id
        self.output_id = output_id
        super().__init__()

    @functools.cached_property
    def _params(self) -> dict:
        params = super()._params
        if self.input_id:
            params["input"] = self.input_id
        else:
            params["output"] = cast(int, self.output_id)

        return params
