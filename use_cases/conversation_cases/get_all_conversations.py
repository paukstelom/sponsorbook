
from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorCollection

from models.conversation_models import Conversation
from models.ticket_models import Ticket


async def get_conversations(conversations: AsyncIOMotorCollection,
                            page_size: int = 100) -> AsyncGenerator[Conversation, None]:
    for conversation in await conversations.find().to_list(page_size):
        yield Conversation.parse_obj(conversation)
