from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import UserNotFound


async def delete_user(
        database: AsyncIOMotorDatabase,
        user_id: str) -> None:
    res = await database.users.update_one({'_id': user_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise UserNotFound
