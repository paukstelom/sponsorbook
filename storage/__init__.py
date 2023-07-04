from typing import Annotated

import motor.motor_asyncio as ma
from fastapi import Depends

from storage import CollectionRepository
from storage.CollectionRepository import CollectionRepository


async def get_db_session() -> ma.AsyncIOMotorClientSession:
    client = ma.AsyncIOMotorClient(replicaset="rs0")

    async with await client.start_session() as session:
        async with session.start_transaction():
            yield session


DatabaseSessionDep = Annotated[ma.AsyncIOMotorClientSession, Depends(get_db_session)]


async def get_db(session: DatabaseSessionDep) -> ma.AsyncIOMotorDatabase:
    return session.client["sponsorbook"]


DatabaseDep = Annotated[ma.AsyncIOMotorDatabase, Depends(get_db)]


def get_events(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["events"]


def get_contacts(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["contacts"]


def get_sponsors(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["sponsors"]


def get_tickets(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["tickets"]


def get_orgs(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["orgs"]


def get_sub_orgs(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["suborgs"]


def get_categories(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["categories"]


def get_conversations(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["conversations"]


def get_users(db: DatabaseDep) -> ma.AsyncIOMotorCollection:
    return db["users"]


TicketsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_tickets)]
SponsorsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_sponsors)]
EventsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_events)]
OrgsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_orgs)]
ContactsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_contacts)]
SubOrgsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_sub_orgs)]
CategoriesDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_categories)]
ConversationsDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_conversations)]
UsersDep = Annotated[ma.AsyncIOMotorCollection, Depends(get_users)]
