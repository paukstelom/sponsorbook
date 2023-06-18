from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from models.event_models import Event, CreateEventModel


async def create_event(database: AsyncIOMotorDatabase, data: CreateEventModel) -> Event:
    event = Event(
        name=data.name,
        description=data.description,
        sub_organization_ids=data.sub_organization_ids,
    )

    await database.events.insert_one(jsonable_encoder(event))
    return event
