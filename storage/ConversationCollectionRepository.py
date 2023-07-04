from typing import Annotated

import structlog
from fastapi import Depends

from domain import repository as repos
from models.conversation_models import Conversation
from storage import CollectionRepository, ConversationsDep, DatabaseSessionDep


class ConversationCollectionRepository(CollectionRepository[Conversation]):
    def __init__(self, collection: ConversationsDep, session: DatabaseSessionDep):
        super().__init__(collection, session, Conversation)


ConversationRepositoryDep = Annotated[
    repos.ConversationRepository, Depends(ConversationCollectionRepository)
]
