from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=256, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # email unique
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.conversation} at {self.sent_at}"
