from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.organization_models import Organization, CreateOrganizationModel


async def create_organization(
    database: AsyncIOMotorDatabase, data: CreateOrganizationModel
) -> Organization:
    organization = Organization(title=data.title, description=data.description)

    await database.orgs.insert_one(jsonable_encoder(organization))
    return organization
