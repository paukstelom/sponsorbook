from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from dependencies import GetDatabaseDep
from models.py_object_id import PyObjectId
from models.ticket_models import Ticket, CreateTicketModel

router = APIRouter(prefix="/tickets")


@router.post("", response_description="Create a ticket", response_model=Ticket)
async def create_ticket(
        database: GetDatabaseDep, data: CreateTicketModel
) -> Ticket | None:
    res = await database.sponsors.find_one({"_id": data.sponsor_id})
    if res is None:
        raise HTTPException(status_code=400, detail="Sponsor not found!")

    res = await database.events.find_one({"_id": data.event_id})
    if res is None:
        raise HTTPException(status_code=400, detail="Event not found!")

    ticket = Ticket(
        title=data.title,
        description=data.description,
        sponsor_id=PyObjectId(data.sponsor_id),
        event_id=PyObjectId(data.event_id),
    )

    await database.tickets.insert_one(jsonable_encoder(ticket))
    return ticket


@router.get(
    "/{ticket_id}", response_description="Get a ticket", response_model=Optional[Ticket]
)
async def get_ticket(ticket_id: str, database: GetDatabaseDep) -> Optional[Ticket]:
    ticket = await database.tickets.find_one({"_id": ticket_id})

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found!")

    return Ticket.parse_obj(ticket)


@router.get("", response_description="Get all tickets", response_model=List[Ticket])
async def get_tickets(database: GetDatabaseDep, page_size: int = 100) -> List[Ticket]:
    return await database.tickets.find().to_list(page_size)


@router.delete("/{id}", response_description="Archive a ticket", response_model=Ticket)
async def delete_ticket(database: GetDatabaseDep, ticket_id: str) -> None:
    res = await database.tickets.update_one(
        {"_id": ticket_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Ticket not found!")
