from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import OrganizationNotFound
from models.py_object_id import PyObjectId
from models.session import Session
from models.sub_organization_models import CreateSubOrganizationModel, SubOrganization
from models.user_models import User


async def create_sub_organization(
    database: AsyncIOMotorDatabase, data: CreateSubOrganizationModel, user: User
) -> SubOrganization | None:

    res = await database.orgs.find_one({"_id": data.organization_id})
    if res is None:
        raise OrganizationNotFound

    sub_organization = SubOrganization(
        name=data.name,
        description=data.description,
        organization_id=PyObjectId(data.organization_id),
    )

    await database.suborgs.insert_one(jsonable_encoder(sub_organization))
    return sub_organization
