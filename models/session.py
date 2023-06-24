from pydantic import BaseModel, Field


class Session(BaseModel):
    user_id: str = Field()
    logged_in_at: str = Field()
