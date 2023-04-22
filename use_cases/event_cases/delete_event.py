from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import EventNotFound


async def delete_event(events: AsyncIOMotorCollection,
                       id: str) -> None:
    res = await events.update_one({'_id': id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise EventNotFound
