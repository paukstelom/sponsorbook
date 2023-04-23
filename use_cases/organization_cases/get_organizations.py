from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorCollection

from models.organization_models import Organization


async def get_organizations(organizations: AsyncIOMotorCollection,
                            page_size: int = 100) -> AsyncGenerator[Organization, None]:
    for organization in await organizations.find().to_list(page_size):
        yield Organization.parse_obj(organization)
