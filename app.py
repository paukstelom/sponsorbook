from typing import List, Optional

from fastapi import FastAPI, Body, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from models.authentication_models import Credentials
from models.errors import SponsorNotFound, EventNotFound, InvalidCredentials
from models.ticket_models import CreateTicketModel, Ticket
from use_cases.authentication.login import authenticate_user
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncIOMotorClient()
db = client['sponsorbook']

tickets = db['tickets']
sponsors = db['sponsors']
events = db['events']
users = db['users']


@app.post('/login', response_description='Login', response_model=str)
async def login_endpoint(body: Credentials = Body(...)):
    try:
        token = authenticate_user(body)
        return token
    except InvalidCredentials:
        raise HTTPException(status_code=403, detail='Bad credentials')


@app.post('/tickets', response_description="Create a ticket", response_model=Ticket)
async def create_ticket_endpoint(body: CreateTicketModel = Body(...)):
    try:
        ticket = await create_ticket(tickets, sponsors, events, body)
    except SponsorNotFound:
        raise HTTPException(status_code=400, detail='Sponsor not found')
    except EventNotFound:
        raise HTTPException(status_code=400, detail='Event not found')
    return ticket


@app.get('/tickets/{ticket_id}', response_description="Get a ticket", response_model=Optional[Ticket])
async def get_ticket_endpoint(ticket_id: str):
    ticket = await get_ticket(ticket_id, tickets)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.get('/tickets', response_description="Get all tickets", response_model=List[Ticket])
async def get_tickets_endpoint():
    return [item async for item in get_tickets(tickets)]


@app.delete('/tickets/{id}', response_description="Archive a ticket", response_model=Ticket)
async def delete_ticket_endpoint(ticket_id: str):
    return await delete_ticket(tickets, ticket_id)
