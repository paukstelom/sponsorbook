import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import OrganizationNotFound
from models.organization_models import CreateOrganizationModel
from models.py_object_id import PyObjectId
from tests.defaults import default_organization, sponsorbook_database
from use_cases.organization_cases.create_organization import create_organization
from use_cases.organization_cases.delete_organization import delete_organization
from use_cases.organization_cases.get_all_organizations import get_all_organizations
from use_cases.organization_cases.get_organization import get_organization


async def test_create_organization():
    result = await create_organization(sponsorbook_database, default_organization)

    organization_id = result.id
    assert organization_id is not None


async def test_get_organizations():
    await create_organization(sponsorbook_database, default_organization)
    organization_list = [
        item async for item in get_all_organizations(sponsorbook_database)
    ]

    assert len(organization_list) > 0


async def test_delete_non_existent_organization():
    non_existent_id = PyObjectId()
    with pytest.raises(OrganizationNotFound):
        await delete_organization(sponsorbook_database, str(non_existent_id))


async def test_delete_organization():
    result = await create_organization(sponsorbook_database, default_organization)

    organization_id = result.id
    resp = await delete_organization(sponsorbook_database, str(organization_id))

    assert resp is None

    deleted_organization = await get_organization(
        str(organization_id), sponsorbook_database
    )

    assert deleted_organization.is_archived
