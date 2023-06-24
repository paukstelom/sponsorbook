from argon2 import PasswordHasher
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import OrganizationNotFound
from models.organization_models import Organization
from models.user_models import User, CreateUserModel


async def create_user(
    database: AsyncIOMotorDatabase, data: CreateUserModel, hasher: PasswordHasher
) -> User | None:
    organization = await database.orgs.find_one({"_id": data.organization_id})

    if organization is None:
        raise OrganizationNotFound()

    organization = Organization.parse_obj(organization)

    hashed_password = hasher.hash(data.password)
    user = User(email=data.email, type=data.type, password=hashed_password, organization_id=organization.id)

    await database.users.insert_one(jsonable_encoder(user))
    return user
