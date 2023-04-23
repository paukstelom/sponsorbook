from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection

from models.conversation_models import Conversation, CreateConversationModel
from models.errors import TicketNotFound
from models.py_object_id import PyObjectId


async def create_conversation(
        conversations: AsyncIOMotorCollection,
        tickets: AsyncIOMotorCollection,
        data: CreateConversationModel) -> Conversation | None:
    res = await tickets.find_one({'_id': data.ticket_id})
    if res is None:
        raise TicketNotFound

    conversation = Conversation(title=data.title,
                                description=data.description,
                                ticket_id=PyObjectId(data.ticket_id))

    await conversations.insert_one(jsonable_encoder(conversation))
    return conversation
