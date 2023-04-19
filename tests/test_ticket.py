from motor.motor_asyncio import AsyncIOMotorClient

from models.py_object_id import PyObjectId
from models.ticket import CreateTicketModel
from use_cases.create_ticket import create_ticket
from use_cases.delete_ticket import delete_ticket
from use_cases.get_tickets import get_tickets

client = AsyncIOMotorClient()
db = client['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


async def test_create_ticket():
    model = CreateTicketModel(title="hello", description="world")
    result = await create_ticket(tickets, model)

    ticket_id = result.id
    assert ticket_id is not None


async def test_get_tickets():
    model = CreateTicketModel(title="hello", description="world")
    await create_ticket(tickets, model)
    tickets_list = [item async for item in get_tickets(tickets)]

    assert len(tickets_list) > 0


async def test_delete_non_existent_ticket():
    non_existent_id = PyObjectId()
    res = await delete_ticket(tickets, archived_tickets, str(non_existent_id))

    assert res is None


async def test_delete_ticket():
    model = CreateTicketModel(title="hello", description="world")
    result = await create_ticket(tickets, model)

    ticket_id = result.id
    resp = await delete_ticket(tickets, archived_tickets, str(ticket_id))

    assert resp.title == "hello"
