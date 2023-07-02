from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase, AsyncIOMotorClient


async def get_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient()
    db = client["sponsorbook"]

    async with await client.start_session():
        yield db


DatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


def get_events(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db['events']


def get_sponsors(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db['sponsors']


def get_tickets(db: DatabaseDep) -> AsyncIOMotorCollection:
    return db['tickets']


TicketsDep = Annotated[AsyncIOMotorCollection, Depends(get_tickets)]
SponsorsDep = Annotated[AsyncIOMotorCollection, Depends(get_sponsors)]
EventsDep = Annotated[AsyncIOMotorCollection, Depends(get_events)]
