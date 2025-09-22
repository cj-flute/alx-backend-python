from rest_framework import serializers
from .models import User, Conversation, Message


# Chat Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # expose only safe fields
        fields = ['user_id', 'username', 'email', 'first_name',
                  'last_name', 'phone_number', 'role', 'created_at',]

        def get_full_name(self, obj):
            """SerializerMethodField → returns full name dynamically"""
            return f"{obj.first_name} {obj.last_name}"

        def validate_email(self, value):
            """Example of custom validation using serializers.ValidationError"""
            if not value.endswith(".com"):
                raise serializers.ValidationError(
                    "Email must end with .com")
            return value


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    # Nested serializer for sender details
    sender = serializers.CharField(
        source='sender.username', read_only=True)  # explicit CharField
    message_preview = serializers.SerializerMethodField()  # show first 30 chars

    class Meta:
        model = Message
        fields = ['message_id', 'sender',
                  'conversation', 'message_body', 'sent_at']

    def get_message_preview(self, obj):
        """Return first 30 characters of message"""
        return obj.message_body[:30]


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    # Nested serializer for participant details
    participants = UserSerializer(many=True, read_only=True)
    # Nested serializer for messages in the conversation
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def get_total_messages(self, obj):
        """Count how many messages belong to this conversation"""
        return obj.messages.count()
