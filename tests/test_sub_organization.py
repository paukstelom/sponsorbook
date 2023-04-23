import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import TicketNotFound, OrganizationNotFound, SubOrganizationNotFound
from models.event_models import CreateEventModel
from models.organization_models import CreateOrganizationModel
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel
from models.sub_organization_models import CreateSubOrganizationModel
from models.ticket_models import CreateTicketModel
from use_cases.event_cases.create_event import create_event
from use_cases.organization_cases.create_organization import create_organization
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sub_organization_cases.create_sub_organization import create_sub_organization
from use_cases.sub_organization_cases.delete_sub_organization import delete_sub_organization
from use_cases.sub_organization_cases.get_sub_organization import get_sub_organization
from use_cases.sub_organization_cases.get_sub_organizations import get_sub_organizations
from use_cases.ticket_cases.create_ticket import create_ticket
from use_cases.ticket_cases.delete_ticket import delete_ticket
from use_cases.ticket_cases.get_ticket import get_ticket
from use_cases.ticket_cases.get_tickets import get_tickets

client = AsyncIOMotorClient()
db = client['sponsorbook']
sub_organizations = db['sub_organizations']
sponsors = db['sponsors']
events = db['events']
organizations = db['organizations']


async def test_create_sub_organization():
    organization = await create_organization(organizations, CreateOrganizationModel(title='event title',
                                                                                    description='event desc'))
    model = CreateSubOrganizationModel(title="hello", description="world", organization_id=str(organization.id))
    result = await create_sub_organization(sub_organizations, organizations, model)

    sub_organization_id = result.id
    assert sub_organization_id is not None


async def test_create_sub_organization_non_existent_organization():
    model = CreateSubOrganizationModel(title="hello",
                                       description="world",
                                       organization_id='123456789123123456789123')

    with pytest.raises(SubOrganizationNotFound):
        await create_sub_organization(sub_organizations, organizations, model)


async def test_get_sub_organizations():
    organization = await create_organization(organizations, CreateOrganizationModel(title='event title',
                                                                                    description='event desc'))
    model = CreateSubOrganizationModel(title="hello", description="world", organization_id=str(organization.id))
    await create_sub_organization(sub_organizations, organizations, model)
    organizations_list = [item async for item in get_sub_organizations(sub_organizations)]

    assert len(organizations_list) > 0


async def test_delete_non_existent_sub_organization():
    non_existent_id = PyObjectId()
    with pytest.raises(SubOrganizationNotFound):
        await delete_sub_organization(sub_organizations, str(non_existent_id))


async def test_delete_sub_organization():
    organization = await create_organization(organizations, CreateOrganizationModel(title='event title',
                                                                                    description='event desc'))
    model = CreateSubOrganizationModel(title="hello", description="world", organization_id=str(organization.id))
    result = await create_sub_organization(sub_organizations, organizations, model)

    sub_organization_id = result.id
    resp = await delete_sub_organization(sub_organizations, str(sub_organization_id))

    assert resp is None

    deleted_sub_organization = await get_sub_organization(str(sub_organization_id), sub_organizations)

    assert deleted_sub_organization.is_archived
