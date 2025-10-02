from django.shortcuts import render

from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsParticipantOfConversation
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import MessageFilter
from .pagination import StandardResultsSetPagination

User = get_user_model()

"""
    To return JWT tokens immediately so the
    user doesn't need to log in separately after
    singup.
"""


def get_tokens_for_user(user):
    """
        This function generates a refresh and access token for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])  # allow access without a token
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already taken."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    print(user)
    return Response(
        {"message": "User created successfully!"},
        status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list, retrieve, create conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    # Filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    # You can filter by participants
    filterset_fields = ['participants']

    # Search by conversation name or participant usernames
    search_fields = ['participants__username']

    # Allow ordering by creation time
    ordering_fields = ['created_at']

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

    # Pagination
    pagination_class = StandardResultsSetPagination

    # Filters
    filterset_class = MessageFilter

    # permissions
    permisssion_classes = [IsAuthenticated, IsParticipantOfConversation]

    # Filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]

    # Filter by conversation or sender
    filterset_fields = ['conversation', 'sender']

    # Search inside message content
    search_fields = ['message_body']

    # Allow ordering by timestamp
    ordering_fields = ['sent_at']

    def get_queryset(self):
        """
            Restrict messages to only conversations the user is part of.
        """
        return Message.objects.filter(conversation_participants=self.request.user)

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

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            conversation=conversation,
            sender_id=sender_id,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
