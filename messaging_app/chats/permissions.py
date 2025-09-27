from rest_framework import permissions
from .models import Conversation, Message


class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow users who are part of a conversation
    to view or send messages in it.
    """

    def has_permission(self, request, view):
        # 1. Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj will be a Message or Conversation instance
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        # 2. Check if user is a participant of the conversation
        if request.user in conversation.participants.all():
            # Allow GET (view), POST (send), PUT/PATCH (update), DELETE
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return True

        return False
