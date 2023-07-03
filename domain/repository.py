from typing import Generic, Optional, List, TypeVar

from models.base import EntityModel
from models.category_models import Category
from models.contact_models import Contact
from models.conversation_models import Conversation
from models.event_models import Event
from models.organization_models import Organization
from models.py_object_id import PyObjectId
from models.sponsor_models import Sponsor
from models.sub_organization_models import SubOrganization
from models.ticket_models import Ticket
from models.user_models import User

T = TypeVar("T", bound=EntityModel)


class Repository(Generic[T]):
    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        ...

    async def insert(self, model: T) -> None:
        ...

    async def save(self, model: T) -> None:
        ...

    async def list(self, page_size: int) -> List[T]:
        ...


class OrgRepository(Repository[Organization]):
    ...


class SubOrgRepository(Repository[SubOrganization]):
    ...


class SponsorRepository(Repository[Sponsor]):
    ...


class UserRepository(Repository[User]):
    async def get_by_email(self, email: str) -> Optional[User]:
        ...


class ContactRepository(Repository[Contact]):
    async def list_by_sponsor_id(
        self, sponsor_id: PyObjectId | str, page_size: int = 100
    ) -> List[Contact]:
        ...


class EventRepository(Repository[Event]):
    ...


class TicketRepository(Repository[Ticket]):
    ...


class CategoryRepository(Repository[Category]):
    ...


class ConversationRepository(Repository[Conversation]):
    ...
