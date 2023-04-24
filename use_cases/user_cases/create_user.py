from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import SubOrganizationNotFound
from models.py_object_id import PyObjectId
from models.user_models import User, CreateUserModel


async def create_user(
        users: AsyncIOMotorCollection,
        sub_organizations: AsyncIOMotorCollection,
        data: CreateUserModel) -> User | None:
    res = await sub_organizations.find_one({'_id': data.sub_organization_id})
    if res is None:
        raise SubOrganizationNotFound

    user = User(name=data.name,
                surname=data.surname,
                email=data.email,
                sub_organization_id=PyObjectId(data.sub_organization_id))

    await users.insert_one(jsonable_encoder(user))
    return user
