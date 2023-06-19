from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SponsorNotFound, CategoryNotFound


async def delete_category(database: AsyncIOMotorDatabase, category_id: str) -> None:
    res = await database.categories.update_one(
        {"_id": category_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise CategoryNotFound()
