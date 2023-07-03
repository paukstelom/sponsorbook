from pydantic import Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.py_object_id import PyObjectId


class User(EntityModel):
    organization_id: PyObjectId = Field()
    email: str = Field()
    type: str = Field()
    password: str = Field()

    def is_admin(self):
        return self.type == "Admin"

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateUserModel(BaseCreationModel):
    email: str = Field()
    type: str = Field()
    organization_id: PyObjectId = Field()
    password: str = Field()
