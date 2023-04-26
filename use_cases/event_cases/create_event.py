from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from models.event_models import Event, CreateEventModel


async def create_event(database: AsyncIOMotorDatabase, data: CreateEventModel) -> Event:
    event = Event(title=data.title, description=data.description)

    await database.events.insert_one(jsonable_encoder(event))
    return event

