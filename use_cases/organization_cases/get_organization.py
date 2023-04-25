from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.organization_models import Organization


async def get_organization(organization_id: str, database: AsyncIOMotorDatabase) -> Optional[Organization]:
    organization = await database.orgs.find_one({'_id': organization_id})

    if organization is None:
        return None

    return Organization.parse_obj(organization)
