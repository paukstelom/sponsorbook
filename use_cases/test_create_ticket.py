from pymongo import MongoClient

from use_cases.create_ticket import create_ticket
from use_cases.get_tickets import get_tickets

db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


def test_create_ticket():
    result, code = create_ticket(tickets, {"title": "hello", "description": "world"})

    assert code == 201
    ticket_id = result.get('id')
    assert ticket_id is not None


def test_create_ticket_invalid():
    _, code = create_ticket(tickets, {"title": "hello"})

    assert code == 400


def test_get_tickets():
    create_ticket(tickets, {"title": "hello", "description": "world"})
    tickets_list, code = get_tickets(tickets)

    assert code == 200
    assert len(tickets_list) > 0