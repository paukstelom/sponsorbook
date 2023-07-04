from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClientSession

from domain.repository import ContactRepository
from infrastructure.CollectionRepository import LoggedCollectionRepository
from models.contact_models import Contact
from models.py_object_id import PyObjectId


class ContactCollectionRepository(
    ContactRepository, LoggedCollectionRepository[Contact]
):
    def __init__(
        self, collection: AsyncIOMotorCollection, session: AsyncIOMotorClientSession
    ):
        super().__init__(collection, session, Contact)

    async def list_by_sponsor_id(
        self, _id: PyObjectId | str, page_size: int = 100
    ) -> List[Contact]:
        self.log.info("Getting by sponsor", sponsor_id=_id, page_size=page_size)

        if isinstance(_id, str):
            _id = PyObjectId(_id)

        bsons = await self.collection.find(
            {"sponsor_id": _id, "is_archived": False}
        ).to_list(page_size)

        models_out = []

        for x in bsons:
            models_out.append(self.parser(x))

        self.log.info(
            "Getting by sponsor result",
            models=models_out,
            sponsor_id=_id,
            page_size=page_size,
        )

        return models_out

    async def get_by_email(self, email: str) -> Optional[Contact]:
        contact = await self.collection.find_one({"email": email, "is_archived": False})
        return contact if contact is None else self.parser(contact)
