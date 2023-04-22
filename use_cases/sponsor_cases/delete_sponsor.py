from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import SponsorNotFound


async def delete_sponsor(
        sponsors: AsyncIOMotorCollection,
        id: str) -> None:
    res = await sponsors.update_one({'_id': id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise SponsorNotFound
