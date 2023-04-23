from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.py_object_id import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field()
    surname: str = Field()
    email: str = Field()
    password: str = Field()
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


class CreateUserModel(BaseModel):
    name: str = Field()
    surname: str = Field()
    email: str = Field()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
