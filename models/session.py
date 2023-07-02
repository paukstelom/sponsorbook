from pydantic import BaseModel, Field

from models.user_models import User


class Session(BaseModel):
    user_id: str = Field()
    logged_in_at: str = Field()


class SessionWithUser(BaseModel):
    user: User = Field()
    logged_in_at: str = Field()
