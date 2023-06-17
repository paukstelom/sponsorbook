from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SponsorNotFound


async def delete_sponsor(database: AsyncIOMotorDatabase, sponsor_id: str) -> None:
    res = await database.sponsors.update_one(
        {"_id": sponsor_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise SponsorNotFound
