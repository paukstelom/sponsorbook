import pytest
from argon2 import PasswordHasher

from models.errors import UserNotFound
from models.py_object_id import PyObjectId
from tests.defaults import (
    default_user,
    sponsorbook_database,
)
from use_cases.user_cases.create_user import create_user
from use_cases.user_cases.delete_user import delete_user
from use_cases.user_cases.get_all_users import get_user
from use_cases.user_cases.get_conversations import get_all_users


hasher = PasswordHasher()


async def default_create():
    model = default_user
    return await create_user(sponsorbook_database, model, hasher)


async def test_create_user():
    result = await default_create()

    user_id = result.id
    assert user_id is not None


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
