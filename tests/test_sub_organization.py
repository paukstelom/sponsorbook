import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import OrganizationNotFound, SubOrganizationNotFound
from models.py_object_id import PyObjectId
from tests.defaults import (
    default_organization,
    default_sub_organization,
    sponsorbook_database,
)
from use_cases.organization_cases.create_organization import create_organization
from use_cases.sub_organization_cases.create_sub_organization import (
    create_sub_organization,
)
from use_cases.sub_organization_cases.delete_sub_organization import (
    delete_sub_organization,
)
from use_cases.sub_organization_cases.get_sub_organization import (
    get_sub_organization,
)
from use_cases.sub_organization_cases.get_sub_organizations import get_sub_organizations


async def default_create():
    organization = await create_organization(sponsorbook_database, default_organization)
    model = default_sub_organization(str(organization.id))
    return await create_sub_organization(sponsorbook_database, model)


async def test_create_sub_organization():
    result = await default_create()

    sub_organization_id = result.id
    assert sub_organization_id is not None


async def test_create_sub_organization_non_existent_organization():
    model = default_sub_organization("123456789123123456789123")

    with pytest.raises(OrganizationNotFound):
        await create_sub_organization(sponsorbook_database, model)


async def test_get_sub_organizations():
    await default_create()
    organizations_list = [
        item async for item in get_sub_organizations(sponsorbook_database)
    ]

    assert len(organizations_list) > 0


async def test_delete_non_existent_sub_organization():
    non_existent_id = PyObjectId()
    with pytest.raises(SubOrganizationNotFound):
        await delete_sub_organization(sponsorbook_database, str(non_existent_id))


async def test_delete_sub_organization():
    result = await default_create()

    sub_organization_id = result.id
    resp = await delete_sub_organization(sponsorbook_database, str(sub_organization_id))

    assert resp is None

    deleted_sub_organization = await get_sub_organization(
        str(sub_organization_id), sponsorbook_database
    )

    assert deleted_sub_organization.is_archived
