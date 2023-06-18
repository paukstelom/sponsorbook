from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.conversation_models import Conversation


async def get_conversation(
    conversation_id: str, database: AsyncIOMotorDatabase
) -> Optional[Conversation]:
    conversation = await database.conversations.find_one({"_id": conversation_id})

    if conversation is None:
        return None

    return Conversation.parse_obj(conversation)
