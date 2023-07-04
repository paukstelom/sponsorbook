from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from infrastructure import CollectionRepository
from models.ticket_models import Ticket


class TicketCollectionRepository(CollectionRepository[Ticket]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Ticket)
