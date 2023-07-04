from typing import Annotated, Optional

from fastapi import Depends

from domain import repository as repos
from models.category_models import Category
from storage import CollectionRepository, CategoriesDep, DatabaseSessionDep


class CategoryCollectionRepository(CollectionRepository[Category]):
    def __init__(self, collection: CategoriesDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Category)

    async def get_by_name(self, name: str) -> Optional[Category]:
        collection = await self.collection.find_one(
            {"name": name, "is_archived": False}
        )
        return collection if collection is None else self.parser(collection)


CategoryRepositoryDep = Annotated[
    repos.CategoryRepository, Depends(CategoryCollectionRepository)
]
