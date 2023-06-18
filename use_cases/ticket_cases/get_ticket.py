from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.ticket_models import Ticket


async def get_ticket(
    ticket_id: str, database: AsyncIOMotorDatabase
) -> Optional[Ticket]:
    ticket = await database.tickets.find_one({"_id": ticket_id})

    if ticket is None:
        return None

    return Ticket.parse_obj(ticket)
