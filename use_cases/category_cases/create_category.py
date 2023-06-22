from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.category_models import CreateCategoryModel, Category


async def create_category(
    database: AsyncIOMotorDatabase, data: CreateCategoryModel
) -> Category:
    category = Category(
        name=data.name,
        info=data.info
    )

    await database.categories.insert_one(jsonable_encoder(category))
    return category
