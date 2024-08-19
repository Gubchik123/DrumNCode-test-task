from django_filters.rest_framework import FilterSet

from .models import Book


class BookFilterSet(FilterSet):
    """Filter set for the Book model."""

    class Meta:
        """Meta options for the BookFilterSet."""

        model = Book
        fields = {
            "author": ["exact", "in", "icontains"],
            "published_date": ["exact", "gte", "lte"],
            "language": ["exact", "in", "icontains"],
        }
