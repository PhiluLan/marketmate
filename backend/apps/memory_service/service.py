# backend/apps/memory_service/service.py

from .models import Conversation, Message

class MemoryService:
    @staticmethod
    def get_or_create_conversation(user):
        """
        Gibt eine bestehende Konversation zurück oder legt eine neue an.
        """
        conv, _ = Conversation.objects.get_or_create(user=user)
        return conv

    @staticmethod
    def append_message(conversation, role, content):
        """
        Speichert eine neue Nachricht in der Konversation.
        """
        Message.objects.create(
            conversation=conversation,
            role=role,
            content=content
        )

    @staticmethod
    def get_history(conversation):
        """
        Liefert die gesamte Historie als Liste von dicts:
        [{'role':..., 'content':...}, ...]
        """
        return [
            {"role": m.role, "content": m.content}
            for m in conversation.messages.order_by("timestamp")
        ]
