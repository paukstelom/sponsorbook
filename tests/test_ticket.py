import pytest

from models.errors import SponsorNotFound, TicketNotFound, EventNotFound
from models.py_object_id import PyObjectId
from tests.defaults import (
    default_sponsor,
    default_event,
    default_ticket,
    sponsorbook_database,
)
from use_cases.event_cases.create_event import create_event
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets


async def default_create():
    event = await create_event(sponsorbook_database, default_event)
    sponsor = await create_sponsor(sponsorbook_database, default_sponsor)
    model = default_ticket(str(sponsor.id), str(event.id))
    return await create_ticket(sponsorbook_database, model)


async def test_create_ticket():
    result = await default_create()
    ticket_id = result.id
    assert ticket_id is not None


async def test_create_ticket_non_existent_sponsor():
    event = await create_event(sponsorbook_database, default_event)
    models = default_ticket(
        sponsor_id="123456789123123456789123",
        event_id=str(event.id),
    )
    with pytest.raises(SponsorNotFound):
        await create_ticket(sponsorbook_database, models)


async def test_create_ticket_non_existent_event():
    sponsor = await create_sponsor(sponsorbook_database, default_sponsor)
    models = default_ticket(
        sponsor_id=str(sponsor.id),
        event_id="123456789123123456789123",
    )
    with pytest.raises(EventNotFound):
        await create_ticket(sponsorbook_database, models)


async def test_get_tickets():
    await default_create()
    tickets_list = [item async for item in get_tickets(sponsorbook_database)]

    assert len(tickets_list) > 0


async def test_delete_non_existent_ticket():
    non_existent_id = PyObjectId()
    with pytest.raises(TicketNotFound):
        await delete_ticket(sponsorbook_database, str(non_existent_id))


async def test_delete_ticket():
    result = await default_create()

    ticket_id = result.id
    resp = await delete_ticket(sponsorbook_database, str(ticket_id))

    assert resp is None

    deleted_ticket = await get_ticket(str(ticket_id), sponsorbook_database)

    assert deleted_ticket.is_archived
