from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list, retrieve, create conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create() to allow creating a new conversation with participants.
        Expected payload:
        {
            "participants": [user_id1, user_id2, ...]
        }
        """
        participants = request.data.get("participants", [])
        if not participants or len(participants) < 2:
            return Response(
                {"error": "At least 2 participants are required to create a conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list, retrieve, create messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create() to send a new message in an existing conversation.
        Expected payload:
        {
            "conversation": "conversation_uuid",
            "sender": user_id,
            "message_body": "Hello there!"
        }
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
