from typing import List

from fastapi import APIRouter, Body
from motor.motor_asyncio import AsyncIOMotorClient

from models.sub_organization_models import SubOrganization, CreateSubOrganizationModel
from use_cases.sub_organization_cases.create_sub_organization import (
    create_sub_organization,
)
from use_cases.sub_organization_cases.delete_sub_organization import (
    delete_sub_organization,
)
from use_cases.sub_organization_cases.get_all_sub_organizations import (
    get_sub_organization,
)
from use_cases.sub_organization_cases.get_sub_organizations import get_sub_organizations

router = APIRouter(prefix="/sub_organizations")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get(
    "/",
    response_description="Get sub_organization",
    response_model=List[SubOrganization],
)
async def get_sub_organizations_endpoint():
    return [item async for item in get_sub_organizations(database=db)]


@router.get(
    "/{sub_organization_id}",
    response_description="Get one sub_organization",
    response_model=SubOrganization,
)
async def get_one_sub_organization_endpoint(sub_organization_id: str):
    return await get_sub_organization(
        sub_organization_id=sub_organization_id, database=db
    )


@router.delete("/{sub_organization_id}", response_description="Delete sub_organization")
async def delete_sub_organization_endpoint(sub_organization_id: str):
    await delete_sub_organization(sub_organization_id=sub_organization_id, database=db)


@router.post("/", response_description="Create sub_organization", response_model="")
async def create_sub_organization_endpoint(body: CreateSubOrganizationModel = Body()):
    sub_organization = await create_sub_organization(database=db, data=body)
    return sub_organization
