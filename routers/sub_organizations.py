from typing import List

from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from dependencies import GetUserFromSessionDep
from storage import DatabaseDep, SubOrgsDep, OrgsDep
from models.py_object_id import PyObjectId
from models.sub_organization_models import SubOrganization, CreateSubOrganizationModel

router = APIRouter(prefix="/sub_organizations")


@router.get(
    "",
    response_description="Get sub_organization",
)
async def get_sub_organizations(
    suborgs: SubOrgsDep, page_size: int = 100
) -> List[SubOrganization]:
    return await suborgs.find().to_list(page_size)


@router.get(
    "/{sub_organization_id}",
    response_description="Get one sub_organization",
    response_model=SubOrganization,
)
async def get_sub_organization(
    sub_organization_id: str, suborgs: SubOrgsDep
) -> SubOrganization:
    sub_organization = await suborgs.find_one({"_id": sub_organization_id})

    if sub_organization is None:
        raise HTTPException(status_code=404, detail="Sub-organization not found!")

    return SubOrganization.parse_obj(sub_organization)


@router.delete("/{sub_organization_id}", response_description="Delete sub_organization")
async def delete_sub_organization(
    suborgs: SubOrgsDep, sub_organization_id: str
) -> None:
    res = await suborgs.update_one(
        {"_id": sub_organization_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Sub-organization not found!")


@router.post("", response_description="Create sub_organization", response_model="")
async def create_sub_organization(
    suborgs: SubOrgsDep,
    orgs: OrgsDep,
    user: GetUserFromSessionDep,
    data: CreateSubOrganizationModel = Body(),
) -> SubOrganization | None:
    res = await orgs.find_one({"_id": user.organization_id})
    if res is None:
        raise HTTPException(status_code=404, detail="Sub-organization not found!")

    sub_organization = SubOrganization(
        name=data.name,
        description=data.description,
        organization_id=PyObjectId(user.organization_id),
    )

    await suborgs.insert_one(jsonable_encoder(sub_organization))
    return sub_organization
