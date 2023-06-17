from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.organization_models import Organization


async def get_all_organizations(
    database: AsyncIOMotorDatabase, page_size: int = 100
) -> AsyncGenerator[Organization, None]:
    for organization in await database.orgs.find().to_list(page_size):
        yield Organization.parse_obj(organization)
