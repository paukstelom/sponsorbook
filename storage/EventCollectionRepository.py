from typing import Annotated

import structlog
from fastapi import Depends

from domain import repository as repos
from models.event_models import Event
from storage import CollectionRepository, EventsDep, DatabaseSessionDep


class EventCollectionRepository(CollectionRepository[Event]):
    def __init__(self, collection: EventsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Event)


EventRepositoryDep = Annotated[
    repos.EventRepository, Depends(EventCollectionRepository)
]
