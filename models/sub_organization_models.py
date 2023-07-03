from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.py_object_id import PyObjectId


class SubOrganization(EntityModel):
    name: str = Field()
    description: str = Field()
    is_archived: bool = Field(default=False)
    organization_id: PyObjectId = Field()
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateSubOrganizationModel(BaseCreationModel):
    name: str = Field()
    description: str = Field()
