from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.user_models import User


async def get_user(user_id: str,
                   database: AsyncIOMotorDatabase) -> Optional[User]:
    user = await database.users.find_one({'_id': user_id})

    if user is None:
        return None

    return User.parse_obj(user)
