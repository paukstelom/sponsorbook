from typing import List, Optional, Annotated

from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient

from models.authentication_models import Credentials
from models.errors import SponsorNotFound, EventNotFound, InvalidCredentials
from models.sponsor_models import Sponsor, CreateSponsorModel
from models.ticket_models import CreateTicketModel, Ticket
from use_cases.authentication.login import authenticate_user
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.get_all_sponsors import get_sponsors
from use_cases.sponsor_cases.get_sponsor import get_sponsor
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
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


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.get('/sponsors', response_description='Get sponsors', response_model=List[Sponsor])
async def get_sponsors_endpoint():
    return [item async for item in get_sponsors(database=db)]


@app.get('/sponsor/{sponsor_id}', response_description='Get one sponsor', response_model=Sponsor)
async def get_one_sponsor_endpoint(sponsor_id: str):
    return await get_sponsor(sponsor_id=sponsor_id, database=db)


@app.post('/sponsor/{sponsor_id', response_description='Delete sponsor', response_model=Sponsor)
async def delete_sponsor_endpoint(sponsor_id: str):
    return await delete_sponsor(sponsor_id=sponsor_id, database=db)


@app.post('/sponsors', response_description='Create sponsor', response_model='')
async def create_sponsor_endpoint(body: CreateSponsorModel = Body(...)):
    sponsor = await create_sponsor(database=db, data=body)
    return sponsor


@app.get('/tickets', response_description="Create a ticket", response_model=Ticket)
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
    return [item async for item in get_tickets(db)]


@app.delete('/tickets/{id}', response_description="Archive a ticket", response_model=Ticket)
async def delete_ticket_endpoint(ticket_id: str):
    return await delete_ticket(tickets, ticket_id)
