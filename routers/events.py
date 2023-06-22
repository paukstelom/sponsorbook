from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound, EventNotFound
from models.event_models import CreateEventModel, Event
from use_cases.event_cases.close_event import close_event
from use_cases.event_cases.create_event import create_event
from use_cases.event_cases.delete_event import delete_event
from use_cases.event_cases.get_all_events import get_events
from use_cases.event_cases.get_event import get_event
from use_cases.ticket_cases.get_tickets_for_event import get_event_tickets

router = APIRouter(prefix="/events")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.post("", response_description="Create an event", response_model=Event)
async def create_event_endpoint(body: CreateEventModel = Body(...)):
    try:
        ticket = await create_event(db, body)
    except SponsorNotFound:
        raise HTTPException(status_code=400, detail="Sponsor not found")
    except EventNotFound:
        raise HTTPException(status_code=400, detail="Event not found")
    return ticket


@router.get(
    "/{event_id}", response_description="Get an event", response_model=Optional[Event]
)
async def get_event_endpoint(event_id: str):
    ticket = await get_event(event_id, db)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("", response_description="Get all events", response_model=List[Event])
async def get_events_endpoint():
    return [item async for item in get_events(db)]


@router.delete("/{id}", response_description="Archive an event")
async def delete_event_endpoint(id: str):
    return await delete_event(db, id)


@router.post("/{id}/close", response_description="Close an event")
async def close_event_endpoint(id: str):
    return await close_event(db, id)


@router.get("/{id}/tickets", response_description='Get all tickets related to the event')
async def get_tickets_for_event(id: str):
    return [item async for item in get_event_tickets(database=db, event_id=id)]
