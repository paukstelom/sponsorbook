from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from domain.repository import CategoryRepository
from infrastructure.CollectionRepository import LoggedCollectionRepository
from models.category_models import Category

IS_ARCHIVED_FIELD = "is_archived"


class CategoryCollectionRepository(
    CategoryRepository, LoggedCollectionRepository[Category]
):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Category)

    async def get_by_name(self, name: str) -> Optional[Category]:
        collection = await self.collection.find_one(
            {"name": name, IS_ARCHIVED_FIELD: False}
        )
        return collection if collection is None else self.parser(collection)
