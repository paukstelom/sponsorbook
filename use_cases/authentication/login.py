from datetime import datetime
from typing import Optional

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.authentication_models import Credentials
from models.errors import InvalidCredentials

key = 'secret_key'


async def authenticate_user(
        db: AsyncIOMotorDatabase, credentials: Credentials, hasher: PasswordHasher
) -> Optional[str]:
    user = await db.users.find_one({"email": credentials.email})
    if user is None:
        raise InvalidCredentials()

    try:
        hasher.verify(user['password'], credentials.password)
    except VerifyMismatchError:
        raise InvalidCredentials()

    token = jwt.encode({'user_id': user['_id'],
                        'logged_in_at': str(datetime.now())}, key, algorithm='HS256')
    return token
