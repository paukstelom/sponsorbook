from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.category_models import Category


async def get_one_category(
        category_id: str, database: AsyncIOMotorDatabase
) -> Optional[Category]:
    category = await database.categories.find_one(
        {"_id": category_id, "is_archived": False}
    )

    if category is None:
        return None

    return Category.parse_obj(category)
