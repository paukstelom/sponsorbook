from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.organization_models import Organization


async def get_organization(organization_id: str, organizations: AsyncIOMotorCollection) -> Optional[Organization]:
    organization = await organizations.find_one({'_id': organization_id})

    if organization is None:
        return None

    return Organization.parse_obj(organization)
