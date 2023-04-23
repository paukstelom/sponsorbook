import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import OrganizationNotFound
from models.organization_models import CreateOrganizationModel
from models.py_object_id import PyObjectId
from use_cases.organization_cases.create_organization import create_organization
from use_cases.organization_cases.delete_organization import delete_organization
from use_cases.organization_cases.get_organization import get_organization
from use_cases.organization_cases.get_organizations import get_organizations

client = AsyncIOMotorClient()
db = client['sponsorbook']

organizations = db['organizations']


async def test_create_organization():
    model = CreateOrganizationModel(title="hello", description="world")
    result = await create_organization(organizations, model)

    organization_id = result.id
    assert organization_id is not None


async def test_get_organizations():
    model = CreateOrganizationModel(title="hello", description="world")
    await create_organization(organizations, model)
    organization_list = [item async for item in get_organizations(organizations)]

    assert len(organization_list) > 0


async def test_delete_non_existent_organization():
    non_existent_id = PyObjectId()
    with pytest.raises(OrganizationNotFound):
        await delete_organization(organizations, str(non_existent_id))


async def test_delete_organization():
    model = CreateOrganizationModel(title="hello", description="world")
    result = await create_organization(organizations, model)

    organization_id = result.id
    resp = await delete_organization(organizations, str(organization_id))

    assert resp is None

    deleted_organization = await get_organization(str(organization_id), organizations)

    assert deleted_organization.is_archived
