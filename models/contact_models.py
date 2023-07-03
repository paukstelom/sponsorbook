from pydantic import Field

from models.base import EntityModel, BaseCreationModel, BaseModelConfig
from models.py_object_id import PyObjectId


class CreateContactNestedModel(BaseCreationModel):
    name: str = Field()
    phone: str = Field()
    email: str = Field()
    details: str = Field(default="")


class CreateContactModel(BaseCreationModel):
    name: str = Field()
    sponsor_id: str = Field()
    phone: str = Field()
    email: str = Field()
    details: str = Field(default="")


class Contact(EntityModel):
    name: str = Field()
    sponsor_id: PyObjectId = Field()
    phone: str = Field()
    email: str = Field()
    details: str = Field(default="")

    class Config(BaseModelConfig):
        ...
