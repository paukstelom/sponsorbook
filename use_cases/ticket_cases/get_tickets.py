from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.ticket_models import Ticket


async def get_tickets(database: AsyncIOMotorDatabase,
                      page_size: int = 100) -> AsyncGenerator[Ticket, None]:
    for ticket in await database.tickets.find().to_list(page_size):
        yield Ticket.parse_obj(ticket)
