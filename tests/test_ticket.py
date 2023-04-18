from bson import ObjectId
from pymongo import MongoClient

from use_cases.create_ticket import create_ticket
from use_cases.delete_ticket import delete_ticket
from use_cases.get_ticket import get_ticket
from use_cases.get_tickets import get_tickets

db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


def test_create_ticket():
    result, code = create_ticket(tickets, {"title": "hello", "description": "world"})

    assert code == 201
    ticket_id = result.id
    assert ticket_id is not None


def test_create_ticket_invalid():
    _, code = create_ticket(tickets, {"title": "hello"})

    assert code == 400


def test_get_tickets():
    create_ticket(tickets, {"title": "hello", "description": "world"})
    tickets_list, code = get_tickets(tickets)

    assert code == 200
    assert len(tickets_list) > 0


def test_delete_non_existent_ticket():
    non_existent_id = str(ObjectId())
    _, code = delete_ticket(tickets, archived_tickets, non_existent_id)

    assert code == 400


def test_delete_ticket():
    result, code = create_ticket(tickets, {"title": "hello", "description": "world"})

    ticket_id = result.id
    _, code = delete_ticket(tickets, archived_tickets, ticket_id)

    assert code == 200


def test_get_ticket_id_not_well_formed():
    _, code = get_ticket("abcd", tickets)

    assert code == 400
