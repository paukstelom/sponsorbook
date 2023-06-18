from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.organization_models import Organization, CreateOrganizationModel


async def create_organization(
        database: AsyncIOMotorDatabase, data: CreateOrganizationModel
) -> Organization:
    organization = Organization(name=data.name)

    await database.orgs.insert_one(jsonable_encoder(organization))
    return organization
