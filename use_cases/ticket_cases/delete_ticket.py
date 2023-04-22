from motor.motor_asyncio import AsyncIOMotorCollection

from models.ticket import Ticket


async def delete_ticket(
        tickets: AsyncIOMotorCollection,
        id: str) -> Ticket | None:
    ticket = await tickets.find_one({'_id': id})
    if ticket is None:
        return None

    await tickets.delete_one({'_id': id})
    return Ticket.parse_obj(ticket)
