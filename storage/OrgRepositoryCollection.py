from typing import Annotated

from fastapi import Depends

from domain import repository as repos
from models.organization_models import Organization
from storage import CollectionRepository, OrgsDep, DatabaseSessionDep


class OrgRepositoryCollection(CollectionRepository[Organization]):
    def __init__(self, collection: OrgsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Organization)


OrgRepositoryDep = Annotated[repos.OrgRepository, Depends(OrgRepositoryCollection)]
