from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from models.conversation_models import Conversation


async def get_conversation(id: str, conversations: AsyncIOMotorCollection) -> Optional[Conversation]:
    conversation = await conversations.find_one({'_id': id})

    if conversation is None:
        return None

    return Conversation.parse_obj(conversation)
