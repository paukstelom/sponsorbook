from argon2 import PasswordHasher
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from dependencies import GetSessionDep, GetUserFromSessionDep, GetDatabaseDep
from models.authentication_models import Credentials
from models.errors import InvalidCredentials
from models.session import SessionWithUser
from routers import (
    sponsors,
    tickets,
    events,
    sub_organizations,
    organizations,
    categories,
)
from use_cases.authentication.login import authenticate_user

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(sub_organizations.router)
app.include_router(organizations.router)
app.include_router(categories.router)


@app.post("/login", response_description="Login")
async def login_endpoint(db: GetDatabaseDep, body: Credentials = Body(...)):
    try:
        token = await authenticate_user(db, body, PasswordHasher())
    except InvalidCredentials:
        raise HTTPException(status_code=403, detail="Bad credentials")

    response = Response()
    response.set_cookie(
        key="session", value=token, samesite="none", secure=True, max_age=64 * 64
    )
    return response


@app.get("/session")
async def get_session_endpoint(session: GetSessionDep, user: GetUserFromSessionDep):
    return SessionWithUser(session=session, user=user)
