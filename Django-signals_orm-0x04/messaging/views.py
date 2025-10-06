from django.shortcuts import render, get_object_or_404
import models
from .models import Content, Message
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
