from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure import CollectionRepository
from models.conversation_models import Conversation


class ConversationCollectionRepository(CollectionRepository[Conversation]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Conversation)
