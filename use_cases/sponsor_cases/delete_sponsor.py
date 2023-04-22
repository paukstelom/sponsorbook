from motor.motor_asyncio import AsyncIOMotorCollection

from models.sponsor_models import Sponsor


async def delete_sponsor(
        sponsors: AsyncIOMotorCollection,
        id: str) -> Sponsor | None:
    ticket = await sponsors.find_one({'_id': id})
    if ticket is None:
        return None

    await sponsors.delete_one({'_id': id})
    return Sponsor.parse_obj(ticket)
