import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from models.conversation_models import CreateConversationModel
from models.errors import TicketNotFound, ConversationNotFound
from models.event_models import CreateEventModel
from models.py_object_id import PyObjectId
from models.sponsor_models import CreateSponsorModel, Rating
from models.ticket_models import CreateTicketModel
from use_cases.conversation_cases.create_conversation import create_conversation
from use_cases.conversation_cases.delete_conversation import delete_conversation
from use_cases.conversation_cases.get_all_conversations import get_conversations
from use_cases.conversation_cases.get_conversation import get_conversation
from use_cases.event_cases.create_event import create_event
from use_cases.sponsor_cases.create_sponsor import create_sponsor
from use_cases.ticket_cases.create_ticket import create_ticket

client = AsyncIOMotorClient()
sponsorbook_database = client["sponsorbook"]


async def default_create():
    event = await create_event(
        sponsorbook_database,
        CreateEventModel(name="event title", description="event desc"),
    )

    sponsor = await create_sponsor(
        sponsorbook_database,
        CreateSponsorModel(
            name="sponsor title",
            company_number="123",
            description="sponsor desc",
            website="google.com",
            contacts=list(),
            category="food",
            rating=Rating(score="123", info="bruh"),
        ),
    )

    ticket = await create_ticket(
        sponsorbook_database,
        CreateTicketModel(
            title="hello",
            description="world",
            sponsor_id=str(sponsor.id),
            event_id=str(event.id),
        ),
    )
    model = CreateConversationModel(
        title="hello", description="world", ticket_id=str(ticket.id)
    )
    return await create_conversation(sponsorbook_database, model)


async def test_create_conversation():
    result = await default_create()
    conversation_id = result.id
    assert conversation_id is not None


async def test_create_conversation_non_existent_ticket():
    model = CreateConversationModel(
        title="hello", description="world", ticket_id="123456789123123456789123"
    )
    with pytest.raises(TicketNotFound):
        await create_conversation(sponsorbook_database, model)


async def test_get_conversations():
    await default_create()
    conversation_list = [item async for item in get_conversations(sponsorbook_database)]

    assert len(conversation_list) > 0


async def test_delete_non_existent_conversation():
    non_existent_id = PyObjectId()
    with pytest.raises(ConversationNotFound):
        await delete_conversation(sponsorbook_database, str(non_existent_id))


async def test_delete_conversation():
    result = await default_create()

    conversation_id = result.id
    resp = await delete_conversation(sponsorbook_database, str(conversation_id))

    assert resp is None

    deleted_conversation = await get_conversation(
        str(conversation_id), sponsorbook_database
    )

    assert deleted_conversation.is_archived
