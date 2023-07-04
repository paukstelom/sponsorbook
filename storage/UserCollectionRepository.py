from typing import Optional, Annotated

from fastapi import Depends

from domain import repository as repos
from models.user_models import User
from storage import CollectionRepository, UsersDep, DatabaseSessionDep


class UserCollectionRepository(CollectionRepository[User]):
    def __init__(self, collection: UsersDep, session: DatabaseSessionDep):
        super().__init__(collection, session, User)

    async def get_by_email(self, email: str) -> Optional[User]:
        self.log.info("Getting by email", email=email)
        user = await self.collection.find_one({"email": email})
        return user if user is None else User.parse_obj(user)


UserRepositoryDep = Annotated[repos.UserRepository, Depends(UserCollectionRepository)]
