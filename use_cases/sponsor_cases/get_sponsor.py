from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.sponsor_models import Sponsor


async def get_sponsor(
    sponsor_id: str, database: AsyncIOMotorDatabase
) -> Optional[Sponsor]:
    sponsor = await database.sponsors.find_one({"_id": sponsor_id})

    if sponsor is None:
        return None

    return Sponsor.parse_obj(sponsor)
