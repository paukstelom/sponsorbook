from typing import Annotated

from argon2 import PasswordHasher
from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse, Response

from models.authentication_models import Credentials
from models.errors import InvalidCredentials
from routers import sponsors, tickets, events, sub_organizations, organizations
from use_cases.authentication.login import authenticate_user

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
db = client["sponsorbook"]

app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(sub_organizations.router)
app.include_router(organizations.router)


@app.post("/login", response_description="Login")
async def login_endpoint(body: Credentials = Body(...)):
    try:
        token = await authenticate_user(db, body, PasswordHasher())
        response = Response()
        response.set_cookie(key="session", value=token, samesite="none", secure=True)
        return response
    except InvalidCredentials:
        raise HTTPException(status_code=403, detail="Bad credentials")


@app.get("/items")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
