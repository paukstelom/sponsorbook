from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.event_models import Event, CreateEventModel


async def create_event(events: AsyncIOMotorCollection, data: CreateEventModel) -> Event:
    event = Event(title=data.title, description=data.description)

    await events.insert_one(jsonable_encoder(event))
    return event
