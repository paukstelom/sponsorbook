from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.organization_models import Organization, CreateOrganizationModel


async def create_organization(
        database: AsyncIOMotorDatabase, data: CreateOrganizationModel
) -> Organization:
    organization = Organization(name=data.name)

    result = await database.orgs.insert_one(jsonable_encoder(organization))
    organization = await database.orgs.find_one({"_id": result.inserted_id})

    return Organization.parse_obj(organization)
