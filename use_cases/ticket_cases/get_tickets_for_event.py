from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.ticket_models import Ticket


async def get_event_tickets(database: AsyncIOMotorDatabase, event_id: str, page_size: int = 100) -> AsyncGenerator[Ticket, None]:
    x = event_id
    for ticket in await database.tickets.find().to_list(page_size):
        yield Ticket.parse_obj(ticket)
