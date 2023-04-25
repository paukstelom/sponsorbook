from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.event_models import Event


async def get_events(database: AsyncIOMotorDatabase, page_size: int = 100) -> AsyncGenerator[None, Event]:
    for event in await database.events.find().to_list(page_size):
        yield Event.parse_obj(event)
