from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.category_models import Category


async def get_all_categories(
        database: AsyncIOMotorDatabase, page_size: int = 100
) -> AsyncGenerator[Category, None]:
    for category in await database.categories.find({"is_archived": False}).to_list(
            page_size
    ):
        yield Category.parse_obj(category)
