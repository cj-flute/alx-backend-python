from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow users who are part of a conversation
    to view or send messages in it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is part of the conversation.
        - If obj is a Conversation → check participants.
        - If obj is a Message → check its conversation participants.
        """

        if hasattr(obj, "participants"):  # obj is a Conversation
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # obj is a Message
            return request.user in obj.conversation.participants.all()

        return False
