from motor.motor_asyncio import AsyncIOMotorCollection

from models.errors import ConversationNotFound


async def delete_conversation(
        conversations: AsyncIOMotorCollection,
        id: str) -> None:
    res = await conversations.update_one({'_id': id}, {'$set': {'is_archived': True}})
    if res.matched_count != 1:
        raise ConversationNotFound
