from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import OrganizationNotFound
from models.py_object_id import PyObjectId
from models.sub_organization_models import CreateSubOrganizationModel, SubOrganization


async def create_sub_organization(
        sub_organizations: AsyncIOMotorCollection,
        organizations: AsyncIOMotorCollection,
        data: CreateSubOrganizationModel) -> SubOrganization | None:
    res = await organizations.find_one({'_id': data.organization_id})
    if res is None:
        raise OrganizationNotFound

    sub_organization = SubOrganization(title=data.title,
                                       description=data.description,
                                       organization_id=PyObjectId(data.organization_id))

    await sub_organizations.insert_one(jsonable_encoder(sub_organization))
    return sub_organization
