from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin class for the Book model."""

    list_display = (
        "title",
        "author",
        "isbn",
        "pages",
        "language",
        "published_date",
    )
    search_fields = ("title", "author", "isbn")
    search_help_text = "Search by title, author, or ISBN."
    list_filter = ("author", "published_date", "language")
