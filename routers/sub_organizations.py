from typing import List

from fastapi import APIRouter, Body, HTTPException

from dependencies import RequireUser
from dependencies.infrastructure import OrgRepositoryDep, SubOrgRepositoryDep
from models.sub_organization_models import SubOrganization, CreateSubOrganizationModel

router = APIRouter(prefix="/sub_organizations")


@router.get(
    "",
    response_description="Get sub_organization",
)
async def get_sub_organizations(
    suborgs: SubOrgRepositoryDep, page_size: int = 100
) -> List[SubOrganization]:
    return await suborgs.list(page_size)


@router.get(
    "/{sub_organization_id}",
    response_description="Get one sub_organization",
)
async def get_sub_organization(
    sub_organization_id: str, suborgs: SubOrgRepositoryDep
) -> SubOrganization:
    if (sub_organization := await suborgs.get_by_id(sub_organization_id)) is None:
        raise HTTPException(status_code=404, detail="Sub-organization not found!")

    return sub_organization


@router.delete("/{sub_organization_id}", response_description="Delete sub_organization")
async def delete_sub_organization(
    suborgs: SubOrgRepositoryDep, sub_organization_id: str
) -> None:
    if (suborg := await suborgs.get_by_id(sub_organization_id)) is None:
        raise HTTPException(status_code=404, detail="Sub-organization not found!")

    suborg.archive()
    await suborgs.save(suborg)


@router.post("", response_description="Create sub_organization")
async def create_sub_organization(
    suborgs: SubOrgRepositoryDep,
    orgs: OrgRepositoryDep,
    user: RequireUser,
    data: CreateSubOrganizationModel = Body(),
) -> SubOrganization:
    if (org := await orgs.get_by_id(user.organization_id)) is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    sub_organization = SubOrganization(
        name=data.name,
        description=data.description,
        organization_id=org.id,
    )

    await suborgs.insert(sub_organization)
    return sub_organization
