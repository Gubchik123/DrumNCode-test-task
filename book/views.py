from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer


class BookViewSet(ModelViewSet):
    """ViewSet for the Book model."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
