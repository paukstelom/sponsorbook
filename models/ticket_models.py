from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.py_object_id import PyObjectId


class Ticket(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field()
    description: str = Field()
    is_archived: bool = Field(default=False)
    sponsor_id: PyObjectId = Field()
    event_id: PyObjectId = Field()
    creation_date: datetime = Field(default_factory=datetime.now)
    # last_time_edited: str = Field()
    # editor_id: PyObjectId = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateTicketModel(BaseModel):
    title: str = Field()
    description: str = Field()
    sponsor_id: str = Field()
    event_id: str = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
