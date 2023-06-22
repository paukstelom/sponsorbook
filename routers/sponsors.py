from typing import List

from fastapi import APIRouter, Body
from motor.motor_asyncio import AsyncIOMotorClient

from models.sponsor_models import Sponsor, CreateSponsorModel, EditSponsorModel
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.edit_sponsor import update_sponsor
from use_cases.sponsor_cases.get_all_sponsors import get_sponsors
from use_cases.sponsor_cases.get_sponsor import get_sponsor

router = APIRouter(prefix="/sponsors")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get("", response_description="Get sponsors", response_model=List[Sponsor])
async def get_sponsors_endpoint():
    return [item async for item in get_sponsors(database=db)]


@router.get(
    "/{sponsor_id}", response_description="Get one sponsor", response_model=Sponsor
)
async def get_one_sponsor_endpoint(sponsor_id: str):
    return await get_sponsor(sponsor_id=sponsor_id, database=db)


@router.delete("/{sponsor_id}", response_description="Delete sponsor")
async def delete_sponsor_endpoint(sponsor_id: str):
    await delete_sponsor(sponsor_id=sponsor_id, database=db)


@router.post("", response_description="Create sponsor", response_model="")
async def create_sponsor_endpoint(body: CreateSponsorModel = Body()):
    sponsor = await create_sponsor(database=db, data=body)
    return sponsor


@router.put('/{sponsor_id}', response_description='Edit sponsor', response_model=Sponsor)
async def update_sponsor_endpoint(sponsor_id: str, body: EditSponsorModel = Body()):
    await update_sponsor(database=db, sponsor_id=sponsor_id, changes=body)
    return await get_sponsor(sponsor_id=sponsor_id, database=db)
