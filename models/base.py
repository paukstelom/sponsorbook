from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from models.py_object_id import PyObjectId


class EntityModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    is_archived: bool = Field(default=False)
    creation_date: datetime = Field(default_factory=datetime.now)

    def archive(self):
        self.is_archived = True


class BaseModelConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class BaseCreationModel(BaseModel):
    class Config(BaseModelConfig):
        ...
