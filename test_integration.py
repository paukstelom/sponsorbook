from pprint import pprint

import requests as requests


def test_ticket():

    resp = requests.post("http://localhost:5000/ticket", headers={"Content-Type": "application/json"},
                         json={"title": "hello", "description": "world"})

    assert resp.status_code == 201

    ticket_id = resp.json().get('id')
    assert ticket_id is not None

    resp = requests.get(f'http://localhost:5000/ticket/{ticket_id}', headers={"Content-Type": "application/json"})

    assert resp.status_code == 200

    resp = requests.post("http://localhost:5000/ticket", headers={"Content-Type": "application/json"},
                         json={"title": "hello"})

    assert resp.status_code == 400

    resp = requests.get('http://localhost:5000/tickets', headers={"Content-Type": "application/json"})

    assert resp.status_code == 200




