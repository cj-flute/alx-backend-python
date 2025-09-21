from django.shortcuts import render
from .models import MyModel
from .serializers import MyModelSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
