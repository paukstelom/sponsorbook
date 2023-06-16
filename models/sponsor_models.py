from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from models.contact_models import Contact
from models.py_object_id import PyObjectId


class Sponsor(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field()
    contacts: List[Contact] = Field()
    category: str = Field()
    description: str = Field(default='')
    is_archived: bool = Field(default=False)
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


class CreateSponsorModel(BaseModel):
    name: str = Field()
    description: str = Field(default="")
    contacts: List[Contact] = Field()
    category: str = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
