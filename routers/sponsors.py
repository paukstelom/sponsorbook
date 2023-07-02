from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient

from dependencies import GetDatabaseDep
from models.sponsor_models import Sponsor, CreateSponsorModel, EditSponsorModel

router = APIRouter(prefix="/sponsors")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get("", response_description="Get sponsors")
async def get_sponsors(database: GetDatabaseDep, page_size: int = 100) -> List[Sponsor]:
    return await database.sponsors.find({"is_archived": False}).to_list(page_size)


@router.get(
    "/{sponsor_id}", response_description="Get one sponsor", response_model=Sponsor
)
async def get_sponsor(sponsor_id: str, database: GetDatabaseDep) -> Optional[Sponsor]:
    sponsor = await database.sponsors.find_one(
        {"_id": sponsor_id, "is_archived": False}
    )

    if sponsor is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    return Sponsor.parse_obj(sponsor)


@router.delete("/{sponsor_id}", response_description="Delete sponsor")
async def delete_sponsor(database: GetDatabaseDep, sponsor_id: str) -> None:
    res = await database.sponsors.update_one(
        {"_id": sponsor_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Sponsor not found!")


@router.post("", response_description="Create sponsor", response_model="")
async def create_sponsor(database: GetDatabaseDep, data: CreateSponsorModel) -> Sponsor:
    sponsor = Sponsor(
        name=data.name,
        rating=data.rating,
        company_number=data.company_number,
        website=data.website,
        contacts=data.contacts,
        description=data.description,
        categories=data.categories,
    )

    result = await database["sponsors"].insert_one(jsonable_encoder(sponsor))

    return result.inserted_id


@router.put("/{sponsor_id}", response_description="Edit sponsor")
async def update_sponsor(
    database: GetDatabaseDep, sponsor_id: str, changes: EditSponsorModel
) -> None:
    sponsor = await database.sponsors.find_one({"_id": sponsor_id})

    if sponsor is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    sponsor = Sponsor.parse_obj(sponsor)

    if changes.description is not None:
        sponsor.description = changes.description

    if changes.company_number is not None:
        sponsor.company_number = changes.company_number

    if changes.name is not None:
        sponsor.name = changes.name

    if changes.contacts is not None:
        sponsor.contacts = changes.contacts

    if changes.categories is not None:
        sponsor.category = changes.categories

    if changes.status is not None:
        sponsor.status = changes.status

    if changes.website is not None:
        sponsor.website = changes.website

    await database.sponsors.replace_one({"_id": sponsor_id}, jsonable_encoder(sponsor))
