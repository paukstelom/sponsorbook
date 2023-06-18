from motor.motor_asyncio import AsyncIOMotorClient

from models.conversation_models import CreateConversationModel
from models.event_models import CreateEventModel
from models.organization_models import CreateOrganizationModel
from models.sponsor_models import CreateSponsorModel, Rating
from models.sub_organization_models import CreateSubOrganizationModel
from models.ticket_models import CreateTicketModel
from models.user_models import CreateUserModel

default_organization = CreateOrganizationModel(name="VU")

default_event = CreateEventModel(name="hello", description="world")

default_sponsor = CreateSponsorModel(
    name="sponsor title",
    company_number="123",
    description="sponsor desc",
    website="google.com",
    contacts=list(),
    category="food",
    rating=Rating(score="123", info="bruh"),
)


def default_sub_organization(organization_id: str):
    return CreateSubOrganizationModel(
        name="hello", description="world", organization_id=organization_id
    )


def default_ticket(sponsor_id: str, event_id: str):
    return CreateTicketModel(
        title="hello",
        description="world",
        sponsor_id=str(sponsor_id),
        event_id=str(event_id),
    )


default_user = CreateUserModel(email="123@abc.com", type="Developer")


def default_conversation(ticket_id: str):
    return CreateConversationModel(
        title="hello", description="world", ticket_id=ticket_id
    )


sponsorbook_database = AsyncIOMotorClient()["sponsorbook-test"]
