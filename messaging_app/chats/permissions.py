from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow users who are part of a conversation
    to view or send messages in it.
    """

    def has_object_permission(self, request, view, obj):
        # obj here is a Conversation instance
        return request.user in obj.participants.all()
