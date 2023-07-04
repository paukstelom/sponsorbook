from typing import TypeVar, Optional, List

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from domain.repository import Repository
from infrastructure.WithLogger import WithLogger
from models.base import EntityModel
from models.errors import CouldNotInsert, CouldNotSave
from models.py_object_id import PyObjectId

T = TypeVar("T", bound=EntityModel)


ID_FIELD = "_id"
IS_ARCHIVED_FIELD = "is_archived"

class CollectionRepository(Repository[T]):
    def __init__(
            self,
            collection: AsyncIOMotorCollection,
            session: AsyncIOMotorClientSession,
            type: type[T],
    ):
        super().__init__()
        self.collection = collection
        self.session = session
        self.parser = type.parse_obj

    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        if isinstance(_id, str):
            _id = PyObjectId(_id)

        res = await self.collection.find_one(
            {ID_FIELD: _id, IS_ARCHIVED_FIELD: False}, session=self.session
        )
        return res if res is None else self.parser(res)

    async def insert(self, model: T) -> None:
        res = await self.collection.insert_one(
            model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def insert_many(self, models: List[T]) -> None:
        res = await self.collection.insert_many(
            [x.dict(by_alias=True) for x in models], session=self.session
        )
        if not res.acknowledged:
            raise CouldNotInsert(f"Could not insert {models}")

    async def save(self, model: T) -> None:
        res = await self.collection.replace_one(
            {ID_FIELD: model.id}, model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def list(self, page_size: int) -> List[T]:
        models = await self.collection.find(
            {IS_ARCHIVED_FIELD: False}, session=self.session
        ).to_list(page_size)
        models_out = []
        for x in models:
            models_out.append(self.parser(x))

        return models_out
class LoggedCollectionRepository(CollectionRepository[T], WithLogger):
    def __init__(
            self,
            collection: AsyncIOMotorCollection,
            session: AsyncIOMotorClientSession,
            type: type[T],
    ):
        super().__init__(collection=collection, session=session, type=type)

    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        self.log.info("Getting element by id", id=_id)
        return await super().get_by_id(_id)

    async def insert(self, model: T) -> None:
        self.log.info("Inserting element", model=model.dict())
        await super().insert(model)

    async def insert_many(self, models: List[T]) -> None:
        self.log.info("Inserting elements", model=models)
        await super().insert_many(models)

    async def save(self, model: T) -> None:
        self.log.info("Saving element", model=model.dict())
        await super().save(model)

    async def list(self, page_size: int) -> List[T]:
        self.log.info("Listing elements", page_size=page_size)

        return await super().list(page_size)

