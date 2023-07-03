from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.py_object_id import PyObjectId


class Ticket(EntityModel):
    title: str = Field()
    description: str = Field()
    sponsor_id: PyObjectId = Field()
    event_id: PyObjectId = Field()
    # last_time_edited: str = Field()
    # editor_id: PyObjectId = Field()

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateTicketModel(BaseCreationModel):
    title: str = Field()
    description: str = Field()
    sponsor_id: str = Field()
    event_id: str = Field()
