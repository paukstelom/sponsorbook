import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.get_sponsor import get_sponsor
from use_cases.sponsor_cases.get_sponsors import get_sponsors

client = AsyncIOMotorClient()
db = client['sponsorbook']

sponsors = db['sponsors']


async def test_create_sponsor():
    model = CreateSponsorModel(title="hello", description="world")
    result = await create_sponsor(sponsors, model)

    sponsor_id = result.id
    assert sponsor_id is not None


async def test_get_sponsors():
    model = CreateSponsorModel(title="hello", description="world")
    await create_sponsor(sponsors, model)
    sponsor_list = [item async for item in get_sponsors(sponsors)]

    assert len(sponsor_list) > 0


async def test_delete_non_existent_sponsor():
    non_existent_id = PyObjectId()
    with pytest.raises(SponsorNotFound):
        await delete_sponsor(sponsors, str(non_existent_id))


async def test_delete_sponsor():
    model = CreateSponsorModel(title="hello", description="world")
    result = await create_sponsor(sponsors, model)

    sponsor_id = result.id
    resp = await delete_sponsor(sponsors, str(sponsor_id))

    assert resp is None

    deleted_sponsor = await get_sponsor(str(sponsor_id), sponsors)

    assert deleted_sponsor.is_archived
