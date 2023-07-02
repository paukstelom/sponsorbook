from typing import List

from argon2 import PasswordHasher
from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from storage import DatabaseDep, OrgsDep
from models.organization_models import Organization, CreateOrganizationModel
from models.user_models import CreateUserModel
from use_cases.user_cases.create_user import create_user

router = APIRouter(prefix="/organizations")


@router.get("", response_description="Get organization")
async def get_all_organizations(
    database: DatabaseDep, page_size: int = 100
) -> List[Organization]:
    return await database.orgs.find().to_list(page_size)


@router.get(
    "/{organization_id}",
    response_description="Get one organization",
)
async def get_organization(organization_id: str, orgs: OrgsDep) -> Organization:
    organization = await orgs.find_one({"_id": organization_id})

    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    return organization


@router.delete("/{organization_id}", response_description="Delete organization")
async def delete_organization(orgs: OrgsDep, organization_id: str) -> None:
    res = await orgs.update_one(
        {"_id": organization_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Organization not found!")


@router.post("", response_description="Create organization")
async def create_organization(
    orgs: OrgsDep, db: DatabaseDep, body: CreateOrganizationModel = Body()
):
    organization = Organization(name=body.name)

    result = await orgs.insert_one(jsonable_encoder(organization))
    organization = await orgs.find_one({"_id": result.inserted_id})
    organization = Organization.parse_obj(organization)

    await create_user(
        db,
        CreateUserModel(
            email=body.user_email,
            type="president",
            organization_id=str(organization.id),
            password="qwerty",
        ),
        PasswordHasher(),
    )
