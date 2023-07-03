from datetime import datetime

import jwt
from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, Body, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from dependencies import (
    GetSessionDep,
    GetUserFromSessionDep,
    GetPasswordHasherDep,
)
from storage import DatabaseDep, UserRepositoryDep
from models.authentication_models import Credentials
from models.session import SessionWithUser
from routers import (
    sponsors,
    tickets,
    events,
    sub_organizations,
    organizations,
    categories,
    contacts, users, conversations,
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

key = "secret_key"


@app.post("/login", response_description="Login")
async def login_endpoint(
    users: UserRepositoryDep,
    hasher: GetPasswordHasherDep,
    credentials: Credentials = Body(...),
):
    if (user := await users.get_by_email(credentials.email)) is None:
        raise HTTPException(status_code=403, detail="Bad credentials")

    try:
        hasher.verify(user.password, credentials.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=403, detail="Bad credentials")

    token = jwt.encode(
        {"user_id": str(user.id), "logged_in_at": str(datetime.now())},
        key,
        algorithm="HS256",
    )
    response = Response()
    response.set_cookie(key="session", value=token, max_age=64 * 64)
    return response


@app.get("/session")
async def get_session_endpoint(session: GetSessionDep, user: GetUserFromSessionDep):
    return SessionWithUser(session=session, user=user)
