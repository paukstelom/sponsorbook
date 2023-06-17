from typing import List

from fastapi import APIRouter, Body
from motor.motor_asyncio import AsyncIOMotorClient

from models.organization_models import Organization, CreateOrganizationModel
from models.sub_organization_models import SubOrganization, CreateSubOrganizationModel
from use_cases.organization_cases.create_organization import create_organization
from use_cases.organization_cases.delete_organization import delete_organization
from use_cases.organization_cases.get_all_organizations import get_all_organizations
from use_cases.organization_cases.get_organization import get_organization
from use_cases.sub_organization_cases.create_sub_organization import create_sub_organization
from use_cases.sub_organization_cases.delete_sub_organization import delete_sub_organization
from use_cases.sub_organization_cases.get_all_sub_organizations import get_sub_organization
from use_cases.sub_organization_cases.get_sub_organizations import get_sub_organizations

router = APIRouter(prefix="/organizations")

client = AsyncIOMotorClient()
db = client["sponsorbook"]


@router.get("/", response_description="Get organization", response_model=List[Organization])
async def get_organizations_endpoint():
    return [item async for item in get_all_organizations(database=db)]


@router.get(
    "/{organization_id}", response_description="Get one organization", response_model=Organization
)
async def get_one_organization_endpoint(organization_id: str):
    return await get_organization(organization_id=organization_id, database=db)


@router.delete("/{organization_id}", response_description="Delete organization")
async def delete_organization_endpoint(organization_id: str):
    await delete_organization(organization_id=organization_id, database=db)


@router.post("/", response_description="Create organization", response_model=Organization)
async def create_organization_endpoint(body: CreateOrganizationModel = Body()):
    organization = await create_organization(database=db, data=body)
    return organization

