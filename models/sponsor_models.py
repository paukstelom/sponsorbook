from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field

from models.contact_models import Contact
from models.py_object_id import PyObjectId


class Rating(BaseModel):
    score: str = Field()
    info: str = Field()


class Sponsor(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    company_number: str = Field(alias="companyNumber")
    name: str = Field()
    contacts: List[Contact] = Field()
    website: str = Field()
    category: str = Field()
    rating: Rating = Field()
    description: str = Field()
    is_archived: bool = Field(default=False)
    status: str = Field(default="Available")
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
    company_number: str = Field(alias="companyNumber")
    name: str = Field()
    description: str = Field()
    contacts: List[Contact] = Field()
    category: str = Field()
    rating: Rating = Field()
    website: str = Field()

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
