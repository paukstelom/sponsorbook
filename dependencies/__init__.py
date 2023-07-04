from typing import Annotated

import structlog
from fastapi import Cookie, HTTPException, Depends

from dependencies.infrastructure import UserRepositoryDep
from infrastructure.algorithms import *
from models.errors import UserNotFound
from models.session import Session
from models.user_models import User

logger = structlog.getLogger()


async def get_session_opt(
    session: Annotated[str | None, Cookie()] = None,
) -> Session | None:
    if session is None:
        return None

    key = "secret_key"
    session = Session.parse_obj(jwt.decode(jwt=session, key=key, algorithms=["HS256"]))

    return session


MaybeSession = Annotated[Session | None, Depends(get_session_opt)]


async def get_session(session: MaybeSession) -> Session:
    if session is None:
        raise HTTPException(status_code=403, detail="Session missing")

    return session


RequireSession = Annotated[Session, Depends(get_session)]


async def get_user_from_session_opt(
    users: UserRepositoryDep, session: MaybeSession
) -> User | None:
    return await users.get_by_id(session.user_id)


MaybeUser = Annotated[User | None, Depends(get_user_from_session_opt)]


async def get_user_from_session(user: MaybeUser) -> User:
    if user is None:
        raise UserNotFound()

    return user


RequireUser = Annotated[User, Depends(get_user_from_session)]


async def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


GetPasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]


def get_verify(hasher: GetPasswordHasherDep):
    return Argon2dVerifyPassword(hasher)


VerifyPasswordDep = Annotated[EncodeSession, Depends(get_verify)]


def get_hash(hasher: GetPasswordHasherDep):
    return Argon2dHashPassword(hasher)


HashPasswordDep = Annotated[HashPassword, Depends(get_hash)]

EncodeSessionDep = Annotated[EncodeSession, Depends(JWTEncodeSession)]
