from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import EventNotFound


async def close_event(database: AsyncIOMotorDatabase, event_id: str) -> None:
    res = await database.events.update_one(
        {"_id": event_id}, {"$set": {"status": 'Closed'}}
    )
    if res.matched_count != 1:
        raise EventNotFound()
