from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .filters import BookFilterSet
from .serializers import BookSerializer


class BookViewSet(ModelViewSet):
    """ViewSet for the Book model."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilterSet
