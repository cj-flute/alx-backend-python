from rest_framework import serializers
from .models import User, Conversation, Message


# Chat Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # expose only safe fields
        fields = ['user_id', 'username', 'email', 'first_name',
                  'last_name', 'phone_number', 'role', 'created_at', 'updated_at']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    # Nested serializer for sender details
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender',
                  'conversation', 'message_body', 'sent_at']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    # Nested serializer for participant details
    participants = UserSerializer(many=True, read_only=True)
    # Nested serializer for messages in the conversation
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
