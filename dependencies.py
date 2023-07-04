from datetime import datetime
from typing import Annotated

import jwt
import structlog
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, HTTPException, Depends

from WithLogger import WithLogger
from domain.auth import EncodeSession, HashPassword, VerifyPassword
from models.errors import UserNotFound
from models.session import Session
from models.user_models import User
from storage.UserCollectionRepository import UserRepositoryDep

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


class Argon2dHashPassword(HashPassword):
    def __init__(self, hasher: GetPasswordHasherDep):
        self.hasher = hasher

    def __call__(self, password: str) -> str:
        return self.hasher.hash(password)


class Argon2dVerifyPassword(VerifyPassword, WithLogger):
    def __init__(self, hasher: GetPasswordHasherDep):
        self.hasher = hasher
        super().__init__()

    def __call__(self, password: str, user: User) -> bool:
        self.log.info("Verifying password", user_id=user.id, hash=user.password)

        try:
            self.hasher.verify(user.password, password)
            return True
        except VerifyMismatchError:
            return False


VerifyPasswordDep = Annotated[EncodeSession, Depends(Argon2dVerifyPassword)]
HashPasswordDep = Annotated[HashPassword, Depends(Argon2dHashPassword)]


class JWTEncodeSession(EncodeSession, WithLogger):
    def __init__(self):
        super().__init__()

    def __call__(self, user: User) -> str:
        key = "secret_key"
        self.log.info("Encoding session JWT", user_id=user.id)

        session = Session(user_id=str(user.id), logged_in_at=str(datetime.now()))

        return jwt.encode(
            session.dict(),
            key,
            algorithm="HS256",
        )


EncodeSessionDep = Annotated[EncodeSession, Depends(JWTEncodeSession)]
