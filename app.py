from fastapi import FastAPI, Body
from pymongo import MongoClient

from models.ticket import CreateTicketModel
from use_cases.create_ticket import create_ticket
from use_cases.delete_ticket import delete_ticket
from use_cases.get_ticket import get_ticket
from use_cases.get_tickets import get_tickets

app = FastAPI()
db = MongoClient()['sponsorbook']

tickets = db['tickets']
archived_tickets = db['archived_tickets']


@app.post('/tickets')
def create_ticket_endpoint(body: CreateTicketModel = Body(...)):
    return create_ticket(tickets, body)


@app.get('/tickets/{ticket_id}')
def get_ticket_endpoint(ticket_id: str):
    return get_ticket(ticket_id, tickets)


@app.get('/tickets')
def get_tickets_endpoint():
    return get_tickets(tickets)


@app.delete('/tickets/{id}')
def delete_ticket_endpoint(ticket_id):
    return delete_ticket(tickets, archived_tickets, ticket_id)
