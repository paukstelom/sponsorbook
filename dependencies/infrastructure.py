from typing import Annotated

from fastapi import Depends
from motor import motor_asyncio as ma
from motor.motor_asyncio import AsyncIOMotorCollection

from domain import repository as repos
from infrastructure import get_db_session
from infrastructure.CategoryCollectionRepository import CategoryCollectionRepository
from infrastructure.ContactCollectionRepository import ContactCollectionRepository
from infrastructure.ConversationCollectionRepository import (
    ConversationCollectionRepository,
)
from infrastructure.EventCollectionRepository import EventCollectionRepository
from infrastructure.OrgRepositoryCollection import OrgRepositoryCollection
from infrastructure.SponsorCollectionRepository import SponsorCollectionRepository
from infrastructure.SubOrgCollectionRepository import SubOrgCollectionRepository
from infrastructure.TicketCollectionRepository import TicketCollectionRepository
from infrastructure.UserCollectionRepository import UserCollectionRepository

DatabaseSessionDep = Annotated[ma.AsyncIOMotorClientSession, Depends(get_db_session)]


class GetCollection:
    def __init__(self, name: str):
        self.name = name

    def __call__(self, session: DatabaseSessionDep) -> AsyncIOMotorCollection:
        return session.client["sponsorbook"][self.name]


TicketsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("tickets"))]
SponsorsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("sponsors"))]
EventsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("events"))]
OrgsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("orgs"))]
ContactsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("contacts"))]
SubOrgsDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("suborgs"))]
CategoriesDep = Annotated[
    ma.AsyncIOMotorCollection, Depends(GetCollection("categories"))
]
ConversationsDep = Annotated[
    ma.AsyncIOMotorCollection, Depends(GetCollection("conversations"))
]
UsersDep = Annotated[ma.AsyncIOMotorCollection, Depends(GetCollection("users"))]


def get_contact_repo(session: DatabaseSessionDep, collection: ContactsDep):
    return ContactCollectionRepository(collection, session)


ContactRepositoryDep = Annotated[repos.ContactRepository, Depends(get_contact_repo)]


def get_category_repo(session: DatabaseSessionDep, collection: CategoriesDep):
    return CategoryCollectionRepository(collection, session)


CategoryRepositoryDep = Annotated[repos.CategoryRepository, Depends(get_category_repo)]


def get_conversation_repo(session: DatabaseSessionDep, collection: ConversationsDep):
    return ConversationCollectionRepository(collection, session)


ConversationRepositoryDep = Annotated[
    repos.ConversationRepository, Depends(get_conversation_repo)
]


def get_event_repo(session: DatabaseSessionDep, collection: EventsDep):
    return EventCollectionRepository(collection, session)


EventRepositoryDep = Annotated[repos.EventRepository, Depends(get_event_repo)]


def get_org_repo(session: DatabaseSessionDep, collection: OrgsDep):
    return OrgRepositoryCollection(collection, session)


OrgRepositoryDep = Annotated[repos.OrgRepository, Depends(get_org_repo)]


def get_sponsor_repo(session: DatabaseSessionDep, collection: SponsorsDep):
    return SponsorCollectionRepository(collection, session)


SponsorRepositoryDep = Annotated[repos.SponsorRepository, Depends(get_sponsor_repo)]


def get_suborg_repo(session: DatabaseSessionDep, collection: SubOrgsDep):
    return SubOrgCollectionRepository(collection, session)


SubOrgRepositoryDep = Annotated[repos.SubOrgRepository, Depends(get_suborg_repo)]


def get_ticket_repo(session: DatabaseSessionDep, collection: TicketsDep):
    return TicketCollectionRepository(collection, session)


TicketRepositoryDep = Annotated[repos.TicketRepository, Depends(get_ticket_repo)]


def get_user_repo(session: DatabaseSessionDep, collection: UsersDep):
    return UserCollectionRepository(collection, session)


UserRepositoryDep = Annotated[repos.UserRepository, Depends(get_user_repo)]
