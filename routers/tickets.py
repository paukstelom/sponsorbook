from typing import List

from fastapi import APIRouter, HTTPException

from models.py_object_id import PyObjectId
from models.ticket_models import Ticket, CreateTicketModel
from dependencies.infrastructure import (
    EventRepositoryDep,
    SponsorRepositoryDep,
    TicketRepositoryDep,
)

router = APIRouter(prefix="/tickets")


@router.post("", response_description="Create a ticket")
async def create_ticket(
    tickets: TicketRepositoryDep,
    sponsors: SponsorRepositoryDep,
    events: EventRepositoryDep,
    data: CreateTicketModel,
) -> str:
    if (sponsor := await sponsors.get_by_id(data.sponsor_id)) is None:
        raise HTTPException(status_code=400, detail="Sponsor not found!")

    if (event := await events.get_by_id(data.event_id)) is None:
        raise HTTPException(status_code=400, detail="Event not found!")

    ticket = Ticket(
        title=data.title,
        description=data.description,
        sponsor_id=PyObjectId(sponsor.id),
        event_id=PyObjectId(event.id),
    )

    await tickets.insert(ticket)
    return str(ticket.id)


@router.get("/{ticket_id}", response_description="Get a ticket")
async def get_ticket(ticket_id: str, tickets: TicketRepositoryDep) -> Ticket:
    if (ticket := await tickets.get_by_id(ticket_id)) is None:
        raise HTTPException(status_code=404, detail="Ticket not found!")

    return ticket


@router.get("", response_description="Get all tickets")
async def get_tickets(
    tickets: TicketRepositoryDep, page_size: int = 100
) -> List[Ticket]:
    return await tickets.list(page_size)


@router.delete("/{ticket_id}", response_description="Archive a ticket")
async def delete_ticket(tickets: TicketRepositoryDep, ticket_id: str) -> None:
    if (ticket := await tickets.get_by_id(ticket_id)) is None:
        raise HTTPException(status_code=404, detail="Ticket not found!")

    ticket.archive()

    await tickets.save(ticket)
