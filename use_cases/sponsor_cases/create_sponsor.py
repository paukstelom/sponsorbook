from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.sponsor_models import CreateSponsorModel, Sponsor


async def create_sponsor(database: AsyncIOMotorDatabase, data: CreateSponsorModel) -> Sponsor:
    sponsor = Sponsor(name=data.name,
                      rating=data.rating,
                      company_number=data.company_number,
                      website=data.website,
                      contacts=data.contacts,
                      description=data.description,
                      category=data.category)

    await database.sponsors.insert_one(jsonable_encoder(sponsor))
    return sponsor
