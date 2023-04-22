from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import SponsorNotFound, EventNotFound
from models.py_object_id import PyObjectId
from models.ticket_models import CreateTicketModel, Ticket


async def create_ticket(
        tickets: AsyncIOMotorCollection,
        sponsors: AsyncIOMotorCollection,
        events: AsyncIOMotorCollection,
        data: CreateTicketModel) -> Ticket | None:
    res = await sponsors.find_one({'_id': data.sponsor_id})
    if res is None:
        raise SponsorNotFound

    res = await events.find_one({'_id': data.event_id})
    if res is None:
        raise EventNotFound

    ticket = Ticket(title=data.title,
                    description=data.description,
                    sponsor_id=PyObjectId(data.sponsor_id),
                    event_id=PyObjectId(data.event_id))

    await tickets.insert_one(jsonable_encoder(ticket))
    return ticket
