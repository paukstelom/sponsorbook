from typing import List, Annotated, Optional

import structlog
from fastapi import Depends

from domain import repository as repos
from models.contact_models import Contact
from models.py_object_id import PyObjectId
from storage import CollectionRepository, ContactsDep, DatabaseSessionDep


class ContactCollectionRepository(CollectionRepository[Contact]):
    def __init__(self, collection: ContactsDep, session: DatabaseSessionDep):
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


ContactRepositoryDep = Annotated[
    repos.ContactRepository, Depends(ContactCollectionRepository)
]
