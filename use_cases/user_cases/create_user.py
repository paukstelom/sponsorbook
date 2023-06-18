from argon2 import PasswordHasher
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.user_models import User, CreateUserModel


async def create_user(
    database: AsyncIOMotorDatabase, data: CreateUserModel, hasher: PasswordHasher
) -> User | None:
    hashed_password = hasher.hash(data.password)
    user = User(email=data.email, type=data.type, password=hashed_password)

    await database.users.insert_one(jsonable_encoder(user))
    return user
