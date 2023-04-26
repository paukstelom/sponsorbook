from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import TicketNotFound


async def delete_ticket(database: AsyncIOMotorDatabase,
                        ticket_id: str) -> None:
    res = await database.tickets.update_one({'_id': ticket_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise TicketNotFound
