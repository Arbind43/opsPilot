"""OpsPilot — Conversation Repository"""

from typing import List
from uuid import UUID


from app.models.conversation import Conversation, Message
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    async def get_by_user(self, user_id: UUID) -> List[Conversation]:
        """Get all conversations for a user, ordered by most recent."""
        return await Conversation.find({"user_id": user_id}).sort("-updated_at").to_list()


class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__(Message)

    async def get_by_conversation(self, conversation_id: UUID) -> List[Message]:
        """Get all messages in a conversation, ordered chronologically."""
        return await Message.find({"conversation_id": conversation_id}).sort("+created_at").to_list()
