from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.sponsor_models import Sponsor


async def get_sponsor(id: str, sponsors: AsyncIOMotorCollection) -> Optional[Sponsor]:
    sponsor = await sponsors.find_one({'_id': id})

    if sponsor is None:
        return None

    return Sponsor.parse_obj(sponsor)
