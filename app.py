from datetime import datetime

import jwt
from argon2.exceptions import VerifyMismatchError
from fastapi import FastAPI, Body, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import Response

from dependencies import (
    GetSessionDep,
    GetUserFromSessionDep,
    GetDatabaseDep,
    GetPasswordHasherDep,
)
from models.authentication_models import Credentials
from models.session import SessionWithUser
from routers import (
    sponsors,
    tickets,
    events,
    sub_organizations,
    organizations,
    categories,
)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app.include_router(sponsors.router)
app.include_router(tickets.router)
app.include_router(events.router)
app.include_router(sub_organizations.router)
app.include_router(organizations.router)
app.include_router(categories.router)

key = "secret_key"


@app.post("/login", response_description="Login")
async def login_endpoint(
    db: GetDatabaseDep,
    hasher: GetPasswordHasherDep,
    credentials: Credentials = Body(...),
):
    user = await db.users.find_one({"email": credentials.email})
    if user is None:
        raise HTTPException(status_code=403, detail="Bad credentials")

    try:
        hasher.verify(user["password"], credentials.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=403, detail="Bad credentials")

    token = jwt.encode(
        {"user_id": user["_id"], "logged_in_at": str(datetime.now())},
        key,
        algorithm="HS256",
    )
    response = Response()
    response.set_cookie(
        key="session", value=token, max_age=64 * 64
    )
    return response


@app.get("/session")
async def get_session_endpoint(session: GetSessionDep, user: GetUserFromSessionDep):
    return SessionWithUser(session=session, user=user)
