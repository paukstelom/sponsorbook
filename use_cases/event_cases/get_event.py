from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.event_models import Event


async def get_event(event_id: str, database: AsyncIOMotorDatabase) -> Optional[Event]:
    events = await database.events.find_one({"_id": event_id})

    if events is None:
        return None

    return Event.parse_obj(events)
