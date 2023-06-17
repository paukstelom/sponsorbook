from motor.motor_asyncio import AsyncIOMotorDatabase

from models.errors import ConversationNotFound


async def delete_conversation(
    database: AsyncIOMotorDatabase, conversation_id: str
) -> None:
    res = await database.conversations.update_one(
        {"_id": conversation_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise ConversationNotFound
