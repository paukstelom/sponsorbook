import pytest
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorClient

from models.py_object_id import PyObjectId
from models.ticket import CreateTicketModel
from use_cases.create_ticket import create_ticket
from use_cases.delete_ticket import delete_ticket
from use_cases.get_ticket import get_ticket
from use_cases.get_tickets import get_tickets

client = AsyncIOMotorClient()
db = client['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


async def test_create_ticket():
    model = CreateTicketModel(title="hello", description="world", sponsor_id='123456789123123456789123')
    result = await create_ticket(tickets, model)

    ticket_id = result.id
    assert ticket_id is not None




async def test_create_ticket_invalid_sponsor_id():
    models = CreateTicketModel(title="hello", description="world", sponsor_id='invalid id')
    with pytest.raises(InvalidId):
        result = await create_ticket(tickets, models)


async def test_get_tickets():
    model = CreateTicketModel(title="hello", description="world", sponsor_id='123456789123123456789123')
    await create_ticket(tickets, model)
    tickets_list = [item async for item in get_tickets(tickets)]

    assert len(tickets_list) > 0


async def test_delete_non_existent_ticket():
    non_existent_id = PyObjectId()
    res = await delete_ticket(tickets, str(non_existent_id))

    assert res is None


async def test_delete_ticket():
    model = CreateTicketModel(title="hello", description="world", sponsor_id='123456789123123456789123')
    result = await create_ticket(tickets, model)

    ticket_id = result.id
    resp = await delete_ticket(tickets, str(ticket_id))

    assert resp.title == "hello"

    deleted_ticket = await get_ticket(str(ticket_id), tickets)

    assert deleted_ticket is None
