from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import OrganizationNotFound


async def delete_organization(
        organizations: AsyncIOMotorCollection,
        organization_id: str) -> None:
    res = await organizations.update_one({'_id': organization_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise OrganizationNotFound
