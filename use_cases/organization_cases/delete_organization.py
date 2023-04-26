from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import OrganizationNotFound


async def delete_organization(
        database: AsyncIOMotorDatabase,
        organization_id: str) -> None:
    res = await database.orgs.update_one({'_id': organization_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise OrganizationNotFound
