from typing import Annotated

from fastapi import Depends

from domain import repository as repos
from models.sub_organization_models import SubOrganization
from storage import CollectionRepository, SubOrgsDep, DatabaseSessionDep


class SubOrgCollectionRepository(CollectionRepository[SubOrganization]):
    def __init__(self, collection: SubOrgsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, SubOrganization)


SubOrgRepositoryDep = Annotated[
    repos.SubOrgRepository, Depends(SubOrgCollectionRepository)
]
