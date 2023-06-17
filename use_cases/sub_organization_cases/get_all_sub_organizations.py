from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.sub_organization_models import SubOrganization


async def get_sub_organization(
    sub_organization_id: str, database: AsyncIOMotorDatabase
) -> Optional[SubOrganization]:
    sub_organization = await database.suborgs.find_one({"_id": sub_organization_id})

    if sub_organization is None:
        return None

    return SubOrganization.parse_obj(sub_organization)
