from typing import List, Optional

from fastapi import APIRouter, HTTPException

from models.event_models import CreateEventModel, Event
from models.ticket_models import Ticket
from storage import (
    EventRepositoryDep,
    TicketRepositoryDep,
)

router = APIRouter(prefix="/events")


@router.post("", response_description="Create an event", response_model=Event)
async def create_event(events: EventRepositoryDep, data: CreateEventModel) -> Event:
    event = Event(
        name=data.name,
        description=data.description,
        sub_organization_ids=data.sub_organization_ids,
    )

    await events.insert(event)
    return event


@router.get(
    "/{event_id}", response_description="Get an event", response_model=Optional[Event]
)
async def get_event(events: EventRepositoryDep, event_id: str):
    if (event := await events.get_by_id(event_id)) is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.get("", response_description="Get all events")
async def get_events(events: EventRepositoryDep, page_size: int = 100) -> List[Event]:
    return await events.list(page_size)


@router.delete("/{event_id}", response_description="Archive an event")
async def delete_event(events: EventRepositoryDep, event_id: str) -> None:
    if (event := await events.get_by_id(event_id)) is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.archive()
    await events.save(event)


@router.post("/{event_id}/close", response_description="Close an event")
async def close_event(events: EventRepositoryDep, event_id: str) -> None:
    if (event := await events.get_by_id(event_id)) is None:
        raise HTTPException(status_code=404, detail="Event not found")

    event.close()
    await events.save(event)


@router.get(
    "/{event_id}/tickets", response_description="Get all tickets related to the event"
)
async def get_event_tickets(
    tickets: TicketRepositoryDep, event_id: str, page_size: int = 100
) -> List[Ticket]:
    return await tickets.list(page_size)
