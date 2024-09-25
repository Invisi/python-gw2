import functools

from gw2 import models
from gw2.api._base import AllIdsBase, Base


class WizardsVaultListings(AllIdsBase[models.WizardsVaultListing, int]):
    suffix = "wizardsvault/listings"


class WizardsVaultListing(Base[models.WizardsVaultListing]):
    def __init__(self, listing_id: int):
        self.listing_id = listing_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wizardsvault/listings/{self.listing_id}"


class WizardsVaultObjectives(AllIdsBase[models.WizardsVaultObjective, int]):
    suffix = "wizardsvault/objectives"


class WizardsVaultObjective(Base[models.WizardsVaultObjective]):
    def __init__(self, objective_id: int):
        self.objective_id = objective_id
        super().__init__()

    @functools.cached_property
    def suffix(self) -> str:
        return f"wizardsvault/objectives/{self.objective_id}"
