from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.user_models import User


async def get_all_users(
    database: AsyncIOMotorDatabase, page_size: int = 100
) -> AsyncGenerator[User, None]:
    for user in await database.users.find().to_list(page_size):
        yield User.parse_obj(user)
