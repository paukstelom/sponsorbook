from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import TicketNotFound


async def delete_ticket(
        tickets: AsyncIOMotorCollection,
        id: str) -> None:
    res = await tickets.update_one({'_id': id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise TicketNotFound
