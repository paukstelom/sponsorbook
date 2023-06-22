from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SponsorNotFound
from models.sponsor_models import EditSponsorModel
async def update_sponsor(database: AsyncIOMotorDatabase, sponsor_id: str, changes: EditSponsorModel) -> None:
    new_values = {"$set": changes}
    res = await database.sponsors.replace_one(
        {"_id": sponsor_id}, new_values)
    if res.matched_count != 1:
        raise SponsorNotFound()
