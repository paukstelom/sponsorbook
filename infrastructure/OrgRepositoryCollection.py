from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure import CollectionRepository
from models.organization_models import Organization


class OrgRepositoryCollection(CollectionRepository[Organization]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Organization)
