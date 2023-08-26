import functools

from gw2 import models

from ._base import Base, IdsBase


class Recipes(IdsBase[models.Recipe, int], _type=models.Recipe):
    pass


class Recipe(Base[models.Recipe], _type=models.Recipe):
    def __init__(self, recipe_id: int):
        self.recipe_id = recipe_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"recipes/{self.recipe_id}"
