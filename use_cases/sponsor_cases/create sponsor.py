from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.sponsor_models import CreateSponsorModel, Sponsor


async def create_sponsor(sponsors: AsyncIOMotorCollection, data: CreateSponsorModel) -> Sponsor:
    sponsor = Sponsor(title=data.title, description=data.description)

    await sponsors.insert_one(jsonable_encoder(sponsor))
    return sponsor
