import pytest

from models.errors import EventNotFound
from models.py_object_id import PyObjectId
from routers.events import create_event, get_events, delete_event
from tests.defaults import default_event, sponsorbook_database


async def test_create_event():
    result = await create_event(sponsorbook_database, default_event)

    sponsor_id = result.id
    assert sponsor_id is not None


async def test_get_event():
    await create_event(sponsorbook_database, default_event)
    events_list = await get_events(sponsorbook_database)

    assert len(events_list) > 0


async def test_delete_non_existent_event():
    non_existent_id = PyObjectId()
    with pytest.raises(HttpError):
        await delete_event(sponsorbook_database, str(non_existent_id))


async def test_delete_event():
    result = await create_event(sponsorbook_database, default_event)

    event_id = result.id
    resp = await delete_event(sponsorbook_database, str(event_id))

    assert resp is None

    deleted_event = await get_event(str(event_id), sponsorbook_database)

    assert deleted_event.is_archived
