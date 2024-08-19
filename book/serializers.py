from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    class Meta:
        """Meta options for the BookSerializer."""

        model = Book
        fields = "__all__"
