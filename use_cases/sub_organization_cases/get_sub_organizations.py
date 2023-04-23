from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorCollection

from models.sub_organization_models import SubOrganization


async def get_sub_organizations(sub_organizations: AsyncIOMotorCollection,
                                page_size: int = 100) -> AsyncGenerator[SubOrganization, None]:
    for sub_organization in await sub_organizations.find().to_list(page_size):
        yield SubOrganization.parse_obj(sub_organization)
