from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure import CollectionRepository
from models.sub_organization_models import SubOrganization


class SubOrgCollectionRepository(CollectionRepository[SubOrganization]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, SubOrganization)
