import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SubOrganizationNotFound, UserNotFound
from models.organization_models import CreateOrganizationModel
from models.py_object_id import PyObjectId
from models.sub_organization_models import CreateSubOrganizationModel
from models.user_models import CreateUserModel
from tests.defaults import (
    default_organization,
    default_sub_organization,
    default_user,
    sponsorbook_database,
)
from use_cases.organization_cases.create_organization import create_organization
from use_cases.sub_organization_cases.create_sub_organization import (
    create_sub_organization,
)
from use_cases.user_cases.create_user import create_user
from use_cases.user_cases.delete_user import delete_user
from use_cases.user_cases.get_all_users import get_user
from use_cases.user_cases.get_conversations import get_all_users


async def default_create():
    organization = await create_organization(sponsorbook_database, default_organization)
    sub_organization = await create_sub_organization(
        sponsorbook_database,
        default_sub_organization(
            organization_id=str(organization.id),
        ),
    )

    model = default_user(
        sub_org_id=str(sub_organization.id),
    )
    return await create_user(sponsorbook_database, model)


async def test_create_user():
    result = await default_create()

    user_id = result.id
    assert user_id is not None


async def test_create_user_non_existent_sub_organization():
    model = default_user(
        sub_org_id="123456789123123456789123",
    )
    with pytest.raises(SubOrganizationNotFound):
        await create_user(sponsorbook_database, model)


async def test_get_all_users():
    await default_create()
    users_list = [item async for item in get_all_users(sponsorbook_database)]

    assert len(users_list) > 0


async def test_delete_non_existent_user():
    non_existent_id = PyObjectId()
    with pytest.raises(UserNotFound):
        await delete_user(sponsorbook_database, str(non_existent_id))


async def test_delete_user():
    result = await default_create()

    user_id = result.id
    resp = await delete_user(sponsorbook_database, str(user_id))

    assert resp is None

    deleted_user = await get_user(str(user_id), sponsorbook_database)

    assert deleted_user.is_archived
