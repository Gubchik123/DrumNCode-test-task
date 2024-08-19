from django.db import models


class Book(models.Model):
    """Model representing a book."""

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=50)

    def __str__(self):
        """Returns the title as the string representation of the Book model."""
        return self.title
