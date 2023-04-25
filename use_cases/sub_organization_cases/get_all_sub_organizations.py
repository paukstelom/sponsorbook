from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.sub_organization_models import SubOrganization


async def get_sub_organization(sub_organization_id: str,
                               sub_organizations: AsyncIOMotorCollection) -> Optional[SubOrganization]:
    sub_organization = await sub_organizations.find_one({'_id': sub_organization_id})

    if sub_organization is None:
        return None

    return SubOrganization.parse_obj(sub_organization)
