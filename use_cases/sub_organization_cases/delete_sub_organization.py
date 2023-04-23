from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import SubOrganizationNotFound


async def delete_sub_organization(
        sub_organizations: AsyncIOMotorCollection,
        sub_organization_id: str) -> None:
    res = await sub_organizations.update_one({'_id': sub_organization_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise SubOrganizationNotFound
