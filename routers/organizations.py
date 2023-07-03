from typing import List

from fastapi import APIRouter, Body, HTTPException

from dependencies import GetUserFromSessionDep, GetPasswordHasherDep
from models.organization_models import Organization, CreateOrganizationModel
from models.user_models import User
from storage import DatabaseDep, OrgRepositoryDep, SponsorsDep, UserRepositoryDep

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
async def get_organization(
        organization_id: str, orgs: OrgRepositoryDep, user: GetUserFromSessionDep
) -> Organization:
    if not user.is_admin():
        raise HTTPException(
            status_code=403, detail="User is not allowed to view this resource"
        )
    organization = await orgs.get_by_id(organization_id)

    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    return organization


@router.get(
    "/{organization_id}",
    response_description="Get one organization",
)
async def get_sponsors_for_org(
        organization_id: str, sponsors: SponsorsDep, user: GetUserFromSessionDep
) -> Organization:
    if organization_id != user.organization_id:
        raise HTTPException(
            status_code=403, detail="User is not able to view this resource!"
        )

    return await sponsors.find({"organization_id": organization_id}).to_list()


@router.delete("/{organization_id}", response_description="Delete organization")
async def delete_organization(orgs: OrgRepositoryDep, organization_id: str) -> None:
    org = await orgs.get_by_id(organization_id)

    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    org.archive()
    await orgs.save(org)


@router.post("", response_description="Create organization")
async def create_organization(
        orgs: OrgRepositoryDep,
        users: UserRepositoryDep,
        hasher: GetPasswordHasherDep,
        body: CreateOrganizationModel = Body(),
):
    organization = Organization(name=body.name)
    await orgs.insert(organization)

    hashed_password = hasher.hash("qwerty")
    user = User(
        email=body.user_email,
        type="president",
        password=hashed_password,
        organization_id=organization.id,
    )

    # Send email

    await users.insert(user)
