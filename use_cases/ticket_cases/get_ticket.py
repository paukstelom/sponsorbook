from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.ticket_models import Ticket


async def get_ticket(id: str, tickets: AsyncIOMotorCollection) -> Optional[Ticket]:
    ticket = await tickets.find_one({'_id': id})

    if ticket is None:
        return None

    return Ticket.parse_obj(ticket)
