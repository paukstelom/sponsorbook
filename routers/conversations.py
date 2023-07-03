from typing import List

from fastapi import APIRouter, HTTPException

from models.conversation_models import Conversation, CreateConversationModel
from storage import ConversationRepositoryDep, TicketRepositoryDep

router = APIRouter(prefix="/conversations")


@router.post("", response_description="Create a conversation")
async def create_conversation(
    conversations: ConversationRepositoryDep,
    tickets: TicketRepositoryDep,
    data: CreateConversationModel,
) -> Conversation:
    if (ticket := await tickets.get_by_id(data.ticket_id)) is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    conversation = Conversation(
        title=data.title, description=data.description, ticket_id=ticket.id
    )

    await conversations.insert(conversation)
    return conversation


@router.get("/{conversation_id}", response_description="Get a conversation")
async def get_conversation(
    conversation_id: str, conversations: ConversationRepositoryDep
) -> Conversation:
    if (conversation := await conversations.get_by_id(conversation_id)) is None:
        raise HTTPException(status_code=404, detail="Conversation not found!")

    return conversation


@router.get("", response_description="Get all conversations")
async def get_conversations(
    conversations: ConversationRepositoryDep, page_size: int = 100
) -> List[Conversation]:
    return await conversations.list(page_size)


@router.delete("/{conversation_id}", response_description="Archive a conversation")
async def delete_conversation(
    conversations: ConversationRepositoryDep, conversation_id: str
) -> None:
    if (conversation := await conversations.get_by_id(conversation_id)) is None:
        raise HTTPException(status_code=404, detail="Conversation not found!")

    conversation.archive()

    await conversations.save(conversation)
