from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


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
