from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from models.errors import UserNotFound
from models.session import Session
from models.user_models import User


def get_db() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient()
    db = client["sponsorbook"]

    return db


GetDatabaseDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


async def get_session(
    session: Annotated[str | None, Cookie()] = None,
) -> Session:
    if session is None:
        raise HTTPException(status_code=403, detail="Session missing")

    key = "secret_key"
    session = Session.parse_obj(jwt.decode(jwt=session, key=key, algorithms=["HS256"]))
    return session


GetSessionDep = Annotated[Session, Depends(get_session)]


async def get_user_from_session(db: GetDatabaseDep, session: GetSessionDep) -> User:
    user = await db.users.find_one({"_id": session.user_id})

    if user is None:
        raise UserNotFound()

    return User.parse_obj(user)


GetUserFromSessionDep = Annotated[User, Depends(get_user_from_session)]
