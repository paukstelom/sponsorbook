from datetime import datetime
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from fastapi import Cookie, HTTPException, Depends

from domain.auth import SessionEncoder
from models.errors import UserNotFound
from models.session import Session
from models.user_models import User
from storage import DatabaseDep


async def get_session(
    session: Annotated[str | None, Cookie()] = None,
) -> Session:
    if session is None:
        raise HTTPException(status_code=403, detail="Session missing")

    key = "secret_key"
    session = Session.parse_obj(jwt.decode(jwt=session, key=key, algorithms=["HS256"]))

    return session


GetSessionDep = Annotated[Session, Depends(get_session)]


async def get_user_from_session(db: DatabaseDep, session: GetSessionDep) -> User:
    user = await db.users.find_one({"_id": session.user_id})

    if user is None:
        raise UserNotFound()

    return User.parse_obj(user)


GetUserFromSessionDep = Annotated[User, Depends(get_user_from_session)]


async def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


GetPasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]


class JWTSessionEncoder(SessionEncoder):
    def encode(self, user: User) -> str:
        key = "secret_key"

        return jwt.encode(
            {"user_id": str(user.id), "logged_in_at": str(datetime.now())},
            key,
            algorithm="HS256",
        )


SessionEncoderDep = Annotated[SessionEncoder, Depends(JWTSessionEncoder)]
