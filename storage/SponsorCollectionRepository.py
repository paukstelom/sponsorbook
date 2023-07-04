from typing import Annotated

import structlog
from fastapi import Depends

from domain import repository as repos
from models.sponsor_models import Sponsor
from storage import CollectionRepository, SponsorsDep, DatabaseSessionDep


class SponsorCollectionRepository(CollectionRepository[Sponsor]):
    def __init__(self, collection: SponsorsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Sponsor)


SponsorRepositoryDep = Annotated[
    repos.SponsorRepository, Depends(SponsorCollectionRepository)
]
