from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure import CollectionRepository
from models.event_models import Event


class EventCollectionRepository(CollectionRepository[Event]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Event)
