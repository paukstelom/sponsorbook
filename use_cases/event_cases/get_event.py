from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.event_models import Event


async def get_event(id: str,
                    events: AsyncIOMotorCollection) -> Optional[Event]:
    events = await events.find_one({'_id': id})

    if events is None:
        return None

    return Event.parse_obj(events)
