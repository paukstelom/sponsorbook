from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure.CollectionRepository import LoggedCollectionRepository
from models.sponsor_models import Sponsor


class SponsorCollectionRepository(LoggedCollectionRepository[Sponsor]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Sponsor)
