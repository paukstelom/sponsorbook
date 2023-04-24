from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import UserNotFound


async def delete_user(
        users: AsyncIOMotorCollection,
        user_id: str) -> None:
    res = await users.update_one({'_id': user_id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise UserNotFound
