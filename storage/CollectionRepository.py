from typing import TypeVar, Optional, List

import structlog
from motor import motor_asyncio as motorasync

from WithLogger import WithLogger
from domain import repository as repos
from models.base import EntityModel
from models.errors import CouldNotSave
from models.py_object_id import PyObjectId

T = TypeVar("T", bound=EntityModel)


class CollectionRepository(repos.Repository[T], WithLogger):
    def __init__(
        self,
        collection: motorasync.AsyncIOMotorCollection,
        session: motorasync.AsyncIOMotorClientSession,
        type: type[T],
    ):
        super().__init__()
        self.collection = collection
        self.session = session
        self.parser = type.parse_obj

    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        self.log.info("Getting element by id", id=_id)

        if isinstance(_id, str):
            _id = PyObjectId(_id)

        res = await self.collection.find_one(
            {"_id": _id, "is_archived": False}, session=self.session
        )
        return res if res is None else self.parser(res)

    async def insert(self, model: T) -> None:
        self.log.info("Inserting element", model=model)
        res = await self.collection.insert_one(
            model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def save(self, model: T) -> None:
        self.log.info("Saving element", model=model)
        res = await self.collection.replace_one(
            {"_id": model.id}, model.dict(by_alias=True), session=self.session
        )
        if not res.acknowledged:
            raise CouldNotSave(f"Could not save {model}")

    async def list(self, page_size: int) -> List[T]:
        self.log.info("Listing elements", page_size=page_size)

        models = await self.collection.find(session=self.session).to_list(page_size)
        models_out = []
        for x in models:
            models_out.append(self.parser(x))

        return models_out
