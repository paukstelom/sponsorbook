import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.errors import EventNotFound
from models.event_models import CreateEventModel
from models.py_object_id import PyObjectId
from use_cases.event_cases.create_event import create_event
from use_cases.event_cases.delete_event import delete_event
from use_cases.event_cases.get_all_events import get_events
from use_cases.event_cases.get_event import get_event

client = AsyncIOMotorClient()
sponsorbook_database = client['sponsorbook']


async def test_create_event():
    model = CreateEventModel(title="hello", description="world")
    result = await create_event(sponsorbook_database, model)

    sponsor_id = result.id
    assert sponsor_id is not None


async def test_get_event():
    model = CreateEventModel(title="hello", description="world")
    await create_event(sponsorbook_database, model)
    events_list = [item async for item in get_events(sponsorbook_database)]

    assert len(events_list) > 0


async def test_delete_non_existent_event():
    non_existent_id = PyObjectId()
    with pytest.raises(EventNotFound):
        await delete_event(sponsorbook_database, str(non_existent_id))


async def test_delete_event():
    model = CreateEventModel(title="hello", description="world")
    result = await create_event(sponsorbook_database, model)

    event_id = result.id
    resp = await delete_event(sponsorbook_database, str(event_id))

    assert resp is None

    deleted_event = await get_event(str(event_id), sponsorbook_database)

    assert deleted_event.is_archived
