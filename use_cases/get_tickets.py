
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorCollection

from models.ticket import Ticket


async def get_tickets(tickets: AsyncIOMotorCollection, page_size: int = 100) -> AsyncGenerator[Ticket, None]:
    for ticket in await tickets.find().to_list(page_size):
        yield Ticket.parse_obj(ticket)
