from datetime import datetime

from pydantic import BaseModel, Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel


class Organization(EntityModel):
    name: str = Field()

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateOrganizationModel(BaseCreationModel):
    name: str = Field()
    user_email: str = Field()
