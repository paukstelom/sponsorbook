from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import EventNotFound


async def delete_event(database: AsyncIOMotorDatabase, event_id: str) -> None:
    res = await database.events.update_one(
        {"_id": event_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise EventNotFound
