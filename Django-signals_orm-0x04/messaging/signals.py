from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import User, Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f"Notification created for {instance.receiver.username}")


@receiver(pre_save, sender=Message)
def save_old_message_content(sender, instance, **kwargs):
    """
    Before a message is saved (update), check if the content changed.
    If yes, log the old content into MessageHistory
    """
    if not instance.pk:
        # It's a new message (no previous content to save)
        return

    try:
        # Get the existing message from DB
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Compare content to detect change
    if old_message.content != instance.content:
        # Log old content
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        # Mark message as edited
        instance.edited = True
        print(f"Message '{instance.pk}' was edited. Old version saved.")


@receiver(post_delete, sender=User)
def cleanup_related_data(sender, instance, **kwargs):
    """
    When a User is deleted, clean up all related data manually if needed.
    """
    user = instance

    # Delete sent and received messages
    sent_msgs = Message.objects.filter(sender=user)
    received_msgs = Message.objectsfilter(receiver=user)

    for msg in sent_msgs.union(received_msgs):
        # Delete related histories
        MessageHistory.objects.filter(Message=msg).delete()
        # Delete related notifications
        Notification.objects.filter(message=msg).delete()
        msg.delete()

    # Delete any remaining notifications directly linked to the user
    Notification.objects.filter(user.user).delete()

    print(
        f"All message, notifications, and histories for '{user.username}' have been deleted")
