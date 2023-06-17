from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.py_object_id import PyObjectId


class Event(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field()
    description: str = Field()
    is_archived: bool = Field(default=False)
    status: str = Field(default="Ongoing")
    sub_organization_ids: list[str] = Field(default=[])
    creation_date: datetime = Field(default_factory=datetime.now)

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


class CreateEventModel(BaseModel):
    name: str = Field()
    description: str = Field()
    sub_organization_ids: list[str] = Field(default=[])

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
