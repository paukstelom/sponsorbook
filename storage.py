from typing import Annotated, Optional, List, TypeVar, Generic

from fastapi import Depends
from motor.motor_asyncio import (
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
)

from models.base import EntityModel
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


async def get_db_session() -> AsyncIOMotorClientSession:
    client = AsyncIOMotorClient(replicaset="rs0")

    async with await client.start_session() as session:
        async with session.start_transaction():
            yield session


DatabaseSessionDep = Annotated[AsyncIOMotorClientSession, Depends(get_db_session)]


async def get_db(session: DatabaseSessionDep) -> AsyncIOMotorDatabase:
    return session.client["sponsorbook"]


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


def get_events(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["events"]


def get_contacts(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["contacts"]


def get_sponsors(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["sponsors"]


def get_tickets(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["tickets"]


def get_orgs(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["orgs"]


def get_sub_orgs(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["suborgs"]


def get_categories(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["categories"]


def get_conversations(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["conversations"]


def get_users(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["users"]


TicketsDep = Annotated[AsyncIOMotorCollection, Depends(get_tickets)]
SponsorsDep = Annotated[AsyncIOMotorCollection, Depends(get_sponsors)]
EventsDep = Annotated[AsyncIOMotorCollection, Depends(get_events)]
OrgsDep = Annotated[AsyncIOMotorCollection, Depends(get_orgs)]
ContactsDep = Annotated[AsyncIOMotorCollection, Depends(get_contacts)]
SubOrgsDep = Annotated[AsyncIOMotorCollection, Depends(get_sub_orgs)]
CategoriesDep = Annotated[AsyncIOMotorCollection, Depends(get_categories)]
ConversationsDep = Annotated[AsyncIOMotorCollection, Depends(get_conversations)]
UsersDep = Annotated[AsyncIOMotorCollection, Depends(get_users)]


class CouldNotSave(BaseException):
    ...


T = TypeVar("T", bound=EntityModel)


class CollectionRepository(Generic[T]):
    def __init__(
            self,
            collection: AsyncIOMotorCollection,
            session: AsyncIOMotorClientSession,
            type: type[T],
    ):
        self.collection = collection
        self.session = session
        self.parser = type.parse_obj

    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        if isinstance(_id, str):
            _id = PyObjectId(_id)

        res = await self.collection.find_one({"_id": _id}, session=self.session)
        return res if res is None else self.parser(res)

    async def insert(self, model: T) -> None:
        res = await self.collection.insert_one(
            model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def save(self, model: T) -> None:
        res = await self.collection.replace_one(
            {"_id": model.id}, model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def list(self, page_size: int) -> List[T]:
        models = await self.collection.find(session=self.session).to_list(page_size)
        models_out = []
        for x in models:
            models_out.append(self.parser(x))

        return models_out


class OrgRepository(CollectionRepository[Organization]):
    def __init__(self, collection: OrgsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Organization)


OrgRepositoryDep = Annotated[OrgRepository, Depends()]


class SubOrgRepository(CollectionRepository[SubOrganization]):
    def __init__(self, collection: SubOrgsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, SubOrganization)


SubOrgRepositoryDep = Annotated[SubOrgRepository, Depends()]


class SponsorRepository(CollectionRepository[Sponsor]):
    def __init__(self, collection: SponsorsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Sponsor)


SponsorRepositoryDep = Annotated[SponsorRepository, Depends()]


class UserRepository(CollectionRepository[User]):
    def __init__(self, collection: UsersDep, session: DatabaseSessionDep):
        super().__init__(collection, session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.collection.find_one({"email": email})
        return user if user is None else User.parse_obj(user)


UserRepositoryDep = Annotated[UserRepository, Depends()]


class ContactRepository(CollectionRepository[Contact]):
    def __init__(self, collection: ContactsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Contact)


ContactRepositoryDep = Annotated[ContactRepository, Depends()]


class EventRepository(CollectionRepository[Event]):
    def __init__(self, collection: EventsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Event)


EventRepositoryDep = Annotated[EventRepository, Depends()]


class TicketRepository(CollectionRepository[Ticket]):
    def __init__(self, collection: TicketsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Ticket)


TicketRepositoryDep = Annotated[TicketRepository, Depends()]


class CategoryRepository(CollectionRepository[Category]):
    def __init__(self, collection: CategoriesDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Category)


CategoryRepositoryDep = Annotated[CategoryRepository, Depends()]


class ConversationRepository(CollectionRepository[Conversation]):
    def __init__(self, collection: ConversationsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Conversation)


ConversationRepositoryDep = Annotated[ConversationRepository, Depends()]
