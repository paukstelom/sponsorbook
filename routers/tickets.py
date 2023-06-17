from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound, EventNotFound
from models.ticket_models import Ticket, CreateTicketModel
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets

router = APIRouter(prefix="/tickets")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get("/", response_description="Create a ticket", response_model=Ticket)
async def create_ticket_endpoint(body: CreateTicketModel = Body(...)):
    try:
        ticket = await create_ticket(db, body)
    except SponsorNotFound:
        raise HTTPException(status_code=400, detail="Sponsor not found")
    except EventNotFound:
        raise HTTPException(status_code=400, detail="Event not found")
    return ticket


@router.get(
    "/{ticket_id}", response_description="Get a ticket", response_model=Optional[Ticket]
)
async def get_ticket_endpoint(ticket_id: str):
    ticket = await get_ticket(ticket_id, db)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/", response_description="Get all tickets", response_model=List[Ticket])
async def get_tickets_endpoint():
    return [item async for item in get_tickets(db)]


@router.delete("/{id}", response_description="Archive a ticket", response_model=Ticket)
async def delete_ticket_endpoint(ticket_id: str):
    return await delete_ticket(db, ticket_id)