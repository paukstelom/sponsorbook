from typing import List

from fastapi import APIRouter, Body
from motor.motor_asyncio import AsyncIOMotorClient

from models.category_models import Category, CreateCategoryModel
from models.sponsor_models import Sponsor, CreateSponsorModel
from use_cases.category_cases.create_category import create_category
from use_cases.category_cases.delete_category import delete_category
from use_cases.category_cases.get_all_categories import get_all_categories
from use_cases.category_cases.get_one_category import get_one_category
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.get_all_sponsors import get_sponsors
from use_cases.sponsor_cases.get_sponsor import get_sponsor

router = APIRouter(prefix="/categories")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get("", response_description="Get categories", response_model=List[Category])
async def get_all_categories_endpoint():
    return [item async for item in get_all_categories(database=db)]


@router.get(
    "/{category_id}", response_description="Get one category", response_model=Category
)
async def get_one_category_endpoint(category_id: str):
    return await get_one_category(category_id=category_id, database=db)


@router.delete("/{category_id}", response_description="Delete category")
async def delete_category_endpoint(category_id: str):
    await delete_category(category_id=category_id, database=db)


@router.post("", response_description="Create category", response_model="")
async def create_category_endpoint(body: CreateCategoryModel = Body()):
    category = await create_category(database=db, data=body)
    return category
