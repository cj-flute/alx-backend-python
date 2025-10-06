from rest_framework.pagination import PageNumberPagination
"""
The pagination module defines custom pagination classes for the messaging app.
That determines how many items are displayed per page
"""


class StandardResultsSetPagination(PageNumberPagination):
    """Custom pagination class with standard settings"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


def get_paginated_response(self, data):
    return ({
        'count': self.page.paginator.count,
        'next': self.get_next_link(),
        'previous': self.get_previous_link(),
        'results': data,
    })
