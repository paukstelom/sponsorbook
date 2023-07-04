from abc import ABC, abstractmethod, ABCMeta
from typing import Generic, Optional, List, TypeVar, Sequence

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


class Repository(ABC, Generic[T]):
    @abstractmethod
    async def get_by_id(self, _id: PyObjectId | str) -> Optional[T]:
        ...

    @abstractmethod
    async def insert(self, model: T) -> None:
        ...

    @abstractmethod
    async def insert_many(self, model: List[T]) -> None:
        ...

    @abstractmethod
    async def save(self, model: T) -> None:
        ...

    @abstractmethod
    async def list(self, page_size: int) -> List[T]:
        ...


class OrgRepository(Repository[Organization], ABC):
    ...


class SubOrgRepository(Repository[SubOrganization], ABC):
    ...


class SponsorRepository(Repository[Sponsor], ABC):
    ...


class UserRepository(Repository[User], ABC):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        ...


class ContactRepository(Repository[Contact], ABC):
    @abstractmethod
    async def list_by_sponsor_id(
        self, sponsor_id: PyObjectId | str, page_size: int = 100
    ) -> List[Contact]:
        ...

    @abstractmethod
    async def get_by_email(self, name: str) -> Optional[Contact]:
        ...


class EventRepository(Repository[Event], ABC):
    ...


class TicketRepository(Repository[Ticket], ABC):
    ...


class CategoryRepository(Repository[Category], ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Category]:
        ...


class ConversationRepository(Repository[Conversation], ABC):
    ...
