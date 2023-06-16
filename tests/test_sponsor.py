import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.get_all_sponsors import get_sponsors
from use_cases.sponsor_cases.get_sponsor import get_sponsor

client = AsyncIOMotorClient()
sponsorbook_database = client['sponsorbook']


async def default_create():
    model = CreateSponsorModel(name="hello", category="food", contacts=[])
    return await create_sponsor(sponsorbook_database, model)


async def test_create_sponsor():
    result = await default_create()

    sponsor_id = result.id
    assert sponsor_id is not None


async def test_get_sponsors():
    await default_create()
    sponsor_list = [item async for item in get_sponsors(sponsorbook_database)]

    assert len(sponsor_list) > 0


async def test_delete_non_existent_sponsor():
    non_existent_id = PyObjectId()
    with pytest.raises(SponsorNotFound):
        await delete_sponsor(sponsorbook_database, str(non_existent_id))


async def test_delete_sponsor():
    result = await default_create()
    sponsor_id = result.id
    resp = await delete_sponsor(sponsorbook_database, str(sponsor_id))

    assert resp is None

    deleted_sponsor = await get_sponsor(str(sponsor_id), sponsorbook_database)

    assert deleted_sponsor.is_archived
