from dataclasses import dataclass

from pydantic import BaseModel, Field

from models.py_object_id import PyObjectId


@dataclass
class Ticket(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)


class CreateTicketModel(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
