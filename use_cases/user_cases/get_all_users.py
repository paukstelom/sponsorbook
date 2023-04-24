from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.user_models import User


async def get_user(user_id: str, users: AsyncIOMotorCollection) -> Optional[User]:
    user = await users.find_one({'_id': user_id})

    if user is None:
        return None

    return User.parse_obj(user)
