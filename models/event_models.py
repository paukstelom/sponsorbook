from pydantic import Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.py_object_id import PyObjectId


class Event(EntityModel):
    name: str = Field()
    description: str = Field()
    status: str = Field(default="Ongoing")
    sub_organization_ids: list[PyObjectId] = Field(default=[])

    def close(self):
        self.status = "Closed"

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateEventModel(BaseCreationModel):
    name: str = Field()
    description: str = Field()
    sub_organization_ids: list[str] = Field(default=[])
