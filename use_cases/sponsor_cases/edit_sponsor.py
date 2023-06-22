from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import SponsorNotFound
from models.sponsor_models import EditSponsorModel, Sponsor


async def update_sponsor(database: AsyncIOMotorDatabase, sponsor_id: str, changes: EditSponsorModel) -> None:
    sponsor = await database.sponsors.find_one({"_id": sponsor_id})

    if sponsor.matched_count != 1:
        raise SponsorNotFound()

    sponsor = Sponsor.parse_obj(sponsor)

    if changes.description is not None:
        sponsor.description = changes.description

    if changes.company_number is not None:
        sponsor.company_number = changes.company_number

    if changes.name is not None:
        sponsor.name = changes.name

    if changes.contacts is not None:
        sponsor.contacts = changes.contacts

    if changes.category is not None:
        sponsor.category = changes.category

    if changes.status is not None:
        sponsor.status = changes.status

    if changes.website is not None:
        sponsor.website = changes.website

    res = await database.sponsors.replace_one(
        {"_id": sponsor.id}, jsonable_encoder(sponsor))
