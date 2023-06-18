from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase

from models.conversation_models import Conversation, CreateConversationModel
from models.errors import TicketNotFound
from models.py_object_id import PyObjectId


async def create_conversation(
    database: AsyncIOMotorDatabase, data: CreateConversationModel
) -> Conversation | None:
    res = await database.tickets.find_one({"_id": data.ticket_id})
    if res is None:
        raise TicketNotFound

    conversation = Conversation(
        title=data.title,
        description=data.description,
        ticket_id=PyObjectId(data.ticket_id),
    )

    await database.conversations.insert_one(jsonable_encoder(conversation))
    return conversation
