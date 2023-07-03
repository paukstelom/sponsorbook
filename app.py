from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from routers import (
    sponsors,
    tickets,
    events,
    sub_organizations,
    organizations,
    categories,
    contacts,
    users,
    conversations,
    authentication,
)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(sub_organizations.router)
app.include_router(organizations.router)
app.include_router(categories.router)
app.include_router(contacts.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(authentication.router)
