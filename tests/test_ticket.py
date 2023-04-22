import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound, TicketNotFound
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel
from models.ticket_models import CreateTicketModel
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets

client = AsyncIOMotorClient()
db = client['sponsorbook']
tickets = db['tickets']
sponsors = db['sponsors']


async def test_create_ticket():
    sponsor = await create_sponsor(sponsors, CreateSponsorModel(title='sponsor title', description='sponsor desc'))
    model = CreateTicketModel(title="hello", description="world", sponsor_id=str(sponsor.id))
    result = await create_ticket(tickets, sponsors, model)

    ticket_id = result.id
    assert ticket_id is not None


async def test_create_ticket_non_existent_sponsor():
    models = CreateTicketModel(title="hello", description="world", sponsor_id='123456789123123456789123')
    with pytest.raises(SponsorNotFound):
        await create_ticket(tickets, sponsors, models)


async def test_get_tickets():
    sponsor = await create_sponsor(sponsors, CreateSponsorModel(title='sponsor title', description='sponsor desc'))
    model = CreateTicketModel(title="hello", description="world", sponsor_id=str(sponsor.id))
    await create_ticket(tickets, sponsors, model)
    tickets_list = [item async for item in get_tickets(tickets)]

    assert len(tickets_list) > 0


async def test_delete_non_existent_ticket():
    non_existent_id = PyObjectId()
    with pytest.raises(TicketNotFound):
        await delete_ticket(tickets, str(non_existent_id))


async def test_delete_ticket():
    sponsor = await create_sponsor(sponsors, CreateSponsorModel(title='sponsor title', description='sponsor desc'))
    model = CreateTicketModel(title="hello", description="world", sponsor_id=str(sponsor.id))
    result = await create_ticket(tickets, sponsors, model)

    ticket_id = result.id
    resp = await delete_ticket(tickets, str(ticket_id))

    assert resp is None

    deleted_ticket = await get_ticket(str(ticket_id), tickets)

    assert deleted_ticket.is_archived
