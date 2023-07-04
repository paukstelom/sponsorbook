from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from domain import repository as repos
from domain.repository import ContactRepository, CategoryRepository
from infrastructure.repositories_base import LoggedCollectionRepository, IS_ARCHIVED_FIELD, CollectionRepository
from models.category_models import Category
from models.contact_models import Contact
from models.conversation_models import Conversation
from models.event_models import Event
from models.organization_models import Organization
from models.py_object_id import PyObjectId
from models.sponsor_models import Sponsor
from models.sub_organization_models import SubOrganization
from models.ticket_models import Ticket
from models.user_models import User


class UserCollectionRepository(repos.UserRepository, LoggedCollectionRepository[User]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        self.log.info("Getting by email", email=email)
        user = await self.collection.find_one({"email": email})
        return user if user is None else User.parse_obj(user)


class TicketCollectionRepository(LoggedCollectionRepository[Ticket]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Ticket)


class SubOrgCollectionRepository(LoggedCollectionRepository[SubOrganization]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, SubOrganization)


class SponsorCollectionRepository(LoggedCollectionRepository[Sponsor]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Sponsor)


class OrgRepositoryCollection(LoggedCollectionRepository[Organization]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Organization)


class EventCollectionRepository(LoggedCollectionRepository[Event]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Event)


class ConversationCollectionRepository(LoggedCollectionRepository[Conversation]):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Conversation)


class ContactCollectionRepository(
    ContactRepository, LoggedCollectionRepository[Contact]
):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Contact)

    async def list_by_sponsor_id(
            self, _id: PyObjectId | str, page_size: int = 100
    ) -> List[Contact]:
        self.log.info("Getting by sponsor", sponsor_id=_id, page_size=page_size)

        if isinstance(_id, str):
            _id = PyObjectId(_id)

        bsons = await self.collection.find(
            {"sponsor_id": _id, "is_archived": False}
        ).to_list(page_size)

        models_out = []

        for x in bsons:
            models_out.append(self.parser(x))

        self.log.info(
            "Getting by sponsor result",
            models=models_out,
            sponsor_id=_id,
            page_size=page_size,
        )

        return models_out

    async def get_by_email(self, email: str) -> Optional[Contact]:
        contact = await self.collection.find_one({"email": email, "is_archived": False})
        return contact if contact is None else self.parser(contact)


class CategoryCollectionRepository(
    CategoryRepository, LoggedCollectionRepository[Category]
):
    def __init__(
            self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Category)

    async def get_by_name(self, name: str) -> Optional[Category]:
        collection = await self.collection.find_one(
            {"name": name, IS_ARCHIVED_FIELD: False}
        )
        return collection if collection is None else self.parser(collection)
