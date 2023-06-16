from pydantic import BaseModel, Field


class Contact(BaseModel):
    name: str = Field()
    phone: str = Field()
    email: str = Field()
