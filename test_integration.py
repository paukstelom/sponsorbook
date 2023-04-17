import requests as requests
from bson import ObjectId


def test_get_ticket_id_not_well_formed():
    resp = requests.get(f'http://localhost:5000/tickets/abcd', headers={"Content-Type": "application/json"})

    assert resp.status_code == 400


def test_create_ticket():
    resp = requests.post("http://localhost:5000/tickets", headers={"Content-Type": "application/json"},
                         json={"title": "hello", "description": "world"})

    assert resp.status_code == 201
    ticket_id = resp.json().get('id')
    assert ticket_id is not None


def test_create_ticket_invalid():
    resp = requests.post("http://localhost:5000/tickets", headers={"Content-Type": "application/json"},
                         json={"title": "hello"})

    assert resp.status_code == 400


def test_delete_ticket():
    resp = requests.post("http://localhost:5000/tickets", headers={"Content-Type": "application/json"},
                         json={"title": "hello", "description": "world"})

    ticket_id = resp.json().get('id')
    resp = requests.delete(f'http://localhost:5000/tickets/{ticket_id}', headers={"Content-Type": "application/json"})

    assert resp.status_code == 200


def test_delete_non_existent_ticket():
    non_existent_id = str(ObjectId())
    resp = requests.delete(f'http://localhost:5000/tickets/{non_existent_id}',
                           headers={"Content-Type": "application/json"})

    assert resp.status_code == 400


def test_get_ticket():
    resp = requests.post("http://localhost:5000/tickets", headers={"Content-Type": "application/json"},
                         json={"title": "hello", "description": "world"})

    ticket_id = resp.json().get('id')
    resp = requests.get(f'http://localhost:5000/tickets/{ticket_id}', headers={"Content-Type": "application/json"})

    assert resp.status_code == 200
    ticket = resp.json()
    assert ticket['title'] == "hello"


def test_get_tickets():
    requests.post("http://localhost:5000/tickets", headers={"Content-Type": "application/json"},
                  json={"title": "hello", "description": "world"})

    resp = requests.get('http://localhost:5000/tickets', headers={"Content-Type": "application/json"})

    assert resp.status_code == 200
    assert len(resp.json()) > 0
