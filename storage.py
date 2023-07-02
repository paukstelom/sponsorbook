from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import (
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
    AsyncIOMotorClient,
)


async def get_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient()
    db = client["sponsorbook"]

    async with await client.start_session():
        yield db


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


def get_events(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db["events"]


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


TicketsDep = Annotated[AsyncIOMotorCollection, Depends(get_tickets)]
SponsorsDep = Annotated[AsyncIOMotorCollection, Depends(get_sponsors)]
EventsDep = Annotated[AsyncIOMotorCollection, Depends(get_events)]
OrgsDep = Annotated[AsyncIOMotorCollection, Depends(get_orgs)]
SubOrgsDep = Annotated[AsyncIOMotorCollection, Depends(get_sub_orgs)]
CategoriesDep = Annotated[AsyncIOMotorCollection, Depends(get_categories)]
