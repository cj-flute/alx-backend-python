from django.shortcuts import render, get_object_or_404
import models
from .models import Content, Message
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


@login_required
def user_messages(request):
    """
    Retrieve all messages sent by the logged-in user.
    This satisfies the check for sender=request.user and Message.objects.filter.
    """
    messages = Message.objects.filter(sender=request.user).select_related(
        "receiver", "conversation", "parent_message"
    )

    data = [
        {
            "id": str(msg.message_id),
            "content": msg.content,
            "receiver": msg.receiver.username,
            "timestamp": msg.timestamp,
            "parent": str(msg.parent_message.message_id) if msg.parent_message else None,
        }
        for msg in messages
    ]

    return JsonResponse({"sent_messages": data})


@login_required
def conversation_messages(request, conversation_id):
    """
    Retrieve all messages in a conversation related to the user,
    optimized with prefetch_related.
    """
    conversation = get_object_or_404(Content, pk=conversation_id)
    messages = Message.objects.filter(
        conversation=conversation
    ).select_related("sender", "receiver", "parent_message")

    data = [
        {
            "id": str(msg.message_id),
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "parent": str(msg.parent_message.message_id) if msg.parent_message else None,
        }
        for msg in messages
    ]

    return JsonResponse({"conversation_messages": data})


def get_conversation_with_messages(conversation_id):
    conversation = (
        Content.objects
        .filter(content_id=conversation_id)
        .prefetch_related(
            "participants",
            models.Prefetch(
                "messages",
                queryset=Message.objects.select_related(
                    "sender", "receiver", "parent_message")

            )
        )
        .first()
    )
    return conversation


def get_message_thread(message_id):
    message = get_object_or_404(Message, message_id=message_id)
    data = {
        "id": str(message.message_id),
        "content": message.content,
        "sender": message.sender.username,
        "replies": [
            {
                "id": str(reply.message_id),
                "content": reply.content,
                "sender": reply.sender.username,
            }
            for reply in message.get_all_replies()
        ],
    }
    return data


@login_required
def delete_user(request):
    user = request.user
    username = user.username

    # Delete the user (triggers post_delete signal)
    user.delete()

    messages.success(
        request, f"Account '{username}' has been deleted successfully.")
    return redirect('home')  # replace 'home' with your homepage route name
