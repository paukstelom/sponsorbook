from typing import Annotated

from fastapi import Depends

from domain import repository as repos
from models.ticket_models import Ticket
from storage import CollectionRepository, TicketsDep, DatabaseSessionDep


class TicketCollectionRepository(CollectionRepository[Ticket]):
    def __init__(self, collection: TicketsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Ticket)


TicketRepositoryDep = Annotated[
    repos.TicketRepository, Depends(TicketCollectionRepository)
]
