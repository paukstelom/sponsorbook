import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import SponsorNotFound, EventNotFound
from models.event_models import CreateEventModel
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel
from use_cases.event_cases.create_event import create_event
from use_cases.event_cases.delete_event import delete_event
from use_cases.event_cases.get_events import get_events
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.sponsor_cases.delete_sponsor import delete_sponsor
from use_cases.sponsor_cases.get_sponsor import get_sponsor
from use_cases.sponsor_cases.get_sponsors import get_sponsors

client = AsyncIOMotorClient()
db = client['sponsorbook']

events = db['events']


async def test_create_event():
    model = CreateEventModel(title="hello", description="world")
    result = await create_event(events, model)

    sponsor_id = result.id
    assert sponsor_id is not None


async def test_get_event():
    model = CreateEventModel(title="hello", description="world")
    await create_event(events, model)
    events_list = [item async for item in get_events(events)]

    assert len(events_list) > 0


async def test_delete_non_existent_event():
    non_existent_id = PyObjectId()
    with pytest.raises(EventNotFound):
        await delete_event(events, str(non_existent_id))


async def test_delete_event():
    model = CreateEventModel(title="hello", description="world")
    result = await create_event(events, model)

    event_id = result.id
    resp = await delete_sponsor(events, str(event_id))

    assert resp is None

    deleted_event = await get_sponsor(str(event_id), events)

    assert deleted_event.is_archived
