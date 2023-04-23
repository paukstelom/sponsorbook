from pydantic import BaseModel, Field


class Credentials(BaseModel):
    email: str = Field()
    password: str = Field()

    class Config:
        arbitrary_types_allowed = True
