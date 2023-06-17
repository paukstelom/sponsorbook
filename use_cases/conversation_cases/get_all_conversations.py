from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.conversation_models import Conversation


async def get_conversations(
    database: AsyncIOMotorDatabase, page_size: int = 100
) -> AsyncGenerator[Conversation, None]:
    for conversation in await database.conversations.find().to_list(page_size):
        yield Conversation.parse_obj(conversation)
