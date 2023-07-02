from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from storage import DatabaseDep, EventsDep, TicketsDep
from models.event_models import CreateEventModel, Event
from models.ticket_models import Ticket

router = APIRouter(prefix="/events")


@router.post("", response_description="Create an event", response_model=Event)
async def create_event(database: DatabaseDep, data: CreateEventModel) -> Event:
    event = Event(
        name=data.name,
        description=data.description,
        sub_organization_ids=data.sub_organization_ids,
    )

    await database.events.insert_one(jsonable_encoder(event))
    return event


@router.get(
    "/{event_id}", response_description="Get an event", response_model=Optional[Event]
)
async def get_event(events: EventsDep, event_id: str):
    event = await events.find_one({"_id": event_id})

    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.get("", response_description="Get all events")
async def get_events(events: EventsDep, page_size: int = 100) -> List[Event]:
    return await events.find({"is_archived": False}).to_list(page_size)


@router.delete("/{event_id}", response_description="Archive an event")
async def delete_event(events: EventsDep, event_id: str) -> None:
    res = await events.update_one({"_id": event_id}, {"$set": {"is_archived": True}})
    if res.matched_count != 1:
        raise HTTPException(status_code=403, detail="Session missing")


@router.post("/{id}/close", response_description="Close an event")
async def close_event(events: EventsDep, id: str) -> None:
    res = await events.update_one({"_id": id}, {"$set": {"status": "Closed"}})
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Event not found!")


@router.get(
    "/{event_id}/tickets", response_description="Get all tickets related to the event"
)
async def get_event_tickets(
    tickets: TicketsDep, event_id: str, page_size: int = 100
) -> List[Ticket]:
    return await tickets.find().to_list(page_size)
