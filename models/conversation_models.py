from pydantic import Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.py_object_id import PyObjectId


class Conversation(EntityModel):
    title: str = Field()
    description: str = Field()
    ticket_id: PyObjectId = Field()

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateConversationModel(BaseCreationModel):
    title: str = Field()
    description: str = Field()
    ticket_id: str = Field()
