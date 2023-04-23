from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.organization_models import Organization, CreateOrganizationModel


async def create_organization(organizations: AsyncIOMotorCollection, data: CreateOrganizationModel) -> Organization:
    organization = Organization(title=data.title, description=data.description)

    await organizations.insert_one(jsonable_encoder(organization))
    return organization
