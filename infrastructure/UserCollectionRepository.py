from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from domain import repository as repos
from infrastructure.CollectionRepository import LoggedCollectionRepository
from models.user_models import User


class UserCollectionRepository(repos.UserRepository, LoggedCollectionRepository[User]):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        self.log.info("Getting by email", email=email)
        user = await self.collection.find_one({"email": email})
        return user if user is None else User.parse_obj(user)
