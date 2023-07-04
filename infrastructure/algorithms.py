from datetime import datetime

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from domain.algorithms import HashPassword, VerifyPassword, EncodeSession
from infrastructure.WithLogger import WithLogger
from models.session import Session
from models.user_models import User


class Argon2dHashPassword(HashPassword):
    def __init__(self, hasher: PasswordHasher):
        self.hasher = hasher

    def __call__(self, password: str) -> str:
        return self.hasher.hash(password)


class Argon2dVerifyPassword(VerifyPassword, WithLogger):
    def __init__(self, hasher: PasswordHasher):
        self.hasher = hasher
        super().__init__()

    def __call__(self, password: str, user: User) -> bool:
        self.log.info("Verifying password", user_id=user.id, hash=user.password)

        try:
            self.hasher.verify(user.password, password)
            return True
        except VerifyMismatchError:
            return False


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
