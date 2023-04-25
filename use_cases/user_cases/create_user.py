from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SubOrganizationNotFound
from models.py_object_id import PyObjectId
from models.user_models import User, CreateUserModel


async def create_user(
        database: AsyncIOMotorDatabase,
        data: CreateUserModel) -> User | None:
    res = await database.suborgs.find_one({'_id': data.sub_organization_id})
    if res is None:
        raise SubOrganizationNotFound

    user = User(name=data.name,
                surname=data.surname,
                email=data.email,
                sub_organization_id=PyObjectId(data.sub_organization_id))

    await database.users.insert_one(jsonable_encoder(user))
    return user
