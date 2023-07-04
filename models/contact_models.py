from typing import Optional

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


class CreateContactForSponsorModel(BaseCreationModel):
    name: str = Field()
    phone: str = Field()
    email: str = Field()
    details: str = Field(default="")


class EditContact(BaseCreationModel):
    name: Optional[str] = Field()
    phone: Optional[str] = Field()
    email: Optional[str] = Field()
    details: Optional[str] = Field()


class Contact(EntityModel):
    name: str = Field()
    sponsor_id: PyObjectId = Field()
    phone: str = Field()
    email: str = Field()
    details: str = Field(default="")

    class Config(BaseModelConfig):
        ...
