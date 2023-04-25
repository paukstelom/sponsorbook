from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SubOrganizationNotFound


async def delete_sub_organization(
        database: AsyncIOMotorDatabase,
        sub_organization_id: str) -> None:
    res = await database.suborgs.update_one({'_id': sub_organization_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise SubOrganizationNotFound
