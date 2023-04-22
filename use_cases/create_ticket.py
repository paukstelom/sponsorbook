from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.py_object_id import PyObjectId
from models.ticket import CreateTicketModel, Ticket


async def create_ticket(tickets: AsyncIOMotorCollection, data: CreateTicketModel) -> Ticket:
    ticket = Ticket(title=data.title, description=data.description, sponsor_id=PyObjectId(data.sponsor_id))

    await tickets.insert_one(jsonable_encoder(ticket))
    return ticket
