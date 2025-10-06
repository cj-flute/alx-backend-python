"""
This is a custom filter file to filter the messages
"""
from django_filters import rest_framework as filters
from .models import Message


class MessageFilter(filters.FilterSet):
    """
    Filter class for Message
    Allows filtering messages by sender, conversation, and time range.
    """
    sender = filters.NumberFilter(field_name="sender__id")
    conversation = filters.NumberFilter(
        field_name="conversation__id")
    start_date = filters.DateTimeFilter(
        field_name="sent_at", lookup_expr='gte')
    end_date = filters.DateTimeFilter(
        field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']
