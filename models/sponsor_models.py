from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel
from models.contact_models import CreateContactNestedModel
from models.py_object_id import PyObjectId


class Rating(BaseModel):
    score: str = Field()
    info: str = Field()


class Sponsor(EntityModel):
    company_number: str = Field(alias="companyNumber")
    name: str = Field()
    website: str = Field()
    categories: List[PyObjectId] = Field()
    rating: Rating = Field()
    description: str = Field()
    status: str = Field(default="Available")
    creation_date: datetime = Field(default_factory=datetime.now)

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateSponsorModel(BaseCreationModel):
    company_number: str = Field(alias="companyNumber")
    name: str = Field()
    description: str = Field()
    contacts: List[CreateContactNestedModel] = Field()
    categories: List[str] = Field()
    rating: Rating = Field()
    website: str = Field()


class EditSponsorModel(BaseCreationModel):
    company_number: Optional[str] = Field(alias="companyNumber")
    name: Optional[str] = Field()
    categories: List[str] = Field()
    website: Optional[str] = Field()
    rating: Optional[Rating] = Field()
    description: Optional[str] = Field()
    is_archived: Optional[bool] = Field()
    status: Optional[str] = Field()
