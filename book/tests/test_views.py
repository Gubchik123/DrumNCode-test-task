from django.utils import timezone
from rest_framework.test import APITestCase

from ..models import Book


class BookViewSetAPITestCase(APITestCase):
    """Test cases for the BookViewSet."""

    url = "/api/v1/books/"

    @classmethod
    def setUpTestData(cls):
        """Creates test books."""
        now = timezone.now()
        for count in range(15):
            Book.objects.create(
                title=f"Book {count}",
                author=f"Author {count % 2}",
                published_date=now - timezone.timedelta(days=count),
                isbn=f"9783161484{count}",
                language="English",
            )

    def test_list_books(self):
        """Test that the endpoint returns a list of books."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_list_books_pagination(self):
        """Test that the endpoint returns paginated results."""
        response = self.client.get(self.url)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])
        self.assertIsNone(response.data["previous"])

    def test_list_books_pagination_next(self):
        """Test that the endpoint returns paginated results with next page."""
        response = self.client.get(self.url)
        next_url = response.data["next"]
        response = self.client.get(next_url)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNone(response.data["next"])
        self.assertIsNotNone(response.data["previous"])

    def test_filter_books_by_author_exact(self):
        """Test that the endpoint filters books by author exact."""
        response = self.client.get(self.url, {"author": "Author 0"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 8)
        self.assertEqual(len(response.data["results"]), 8)

    def test_filter_books_by_author_in(self):
        """Test that the endpoint filters books by author in."""
        response = self.client.get(
            self.url, {"author__in": "Author 0,Author 1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filter_books_by_author_icontains(self):
        """Test that the endpoint filters books by author icontains."""
        response = self.client.get(self.url, {"author__icontains": "author"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filter_books_by_published_date_exact(self):
        """Test that the endpoint filters books by published date exact."""
        response = self.client.get(
            self.url, {"published_date": timezone.now().date()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_books_by_published_date_gte(self):
        """Test that the endpoint filters books by published date gte."""
        response = self.client.get(
            self.url, {"published_date__gte": timezone.now().date()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_books_by_published_date_lte(self):
        """Test that the endpoint filters books by published date lte."""
        response = self.client.get(
            self.url, {"published_date__lte": timezone.now().date()}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filter_books_by_language_exact(self):
        """Test that the endpoint filters books by language exact."""
        response = self.client.get(self.url, {"language": "English"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filter_books_by_language_in(self):
        """Test that the endpoint filters books by language in."""
        response = self.client.get(self.url, {"language__in": "English"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_filter_books_by_language_icontains(self):
        """Test that the endpoint filters books by language icontains."""
        response = self.client.get(
            self.url, {"language__icontains": "english"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)

    def test_create_book_valid(self):
        """Test that the endpoint creates a book with valid data."""
        data = self._get_valid_data()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 16)

    def test_create_book_invalid(self):
        """Test that the endpoint does not create a book with invalid data."""
        data = self._get_invalid_data()
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Book.objects.count(), 15)

    def test_retrieve_book(self):
        """Test that the endpoint retrieves a book."""
        book = Book.objects.first()
        response = self.client.get(f"{self.url}{book.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], book.title)

    def test_retrieve_book_not_found(self):
        """Test that the endpoint does not retrieve a non-existent book."""
        response = self.client.get(f"{self.url}999/")
        self.assertEqual(response.status_code, 404)

    def test_update_book_valid(self):
        """Test that the endpoint updates a book with valid data."""
        book = Book.objects.first()
        data = self._get_valid_data()
        response = self.client.put(f"{self.url}{book.pk}/", data)
        self.assertEqual(response.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, data["title"])

    def test_update_book_invalid(self):
        """Test that the endpoint does not update a book with invalid data."""
        book = Book.objects.first()
        data = self._get_invalid_data()
        response = self.client.put(f"{self.url}{book.pk}/", data)
        self.assertEqual(response.status_code, 400)
        book.refresh_from_db()
        self.assertNotEqual(book.title, data["title"])

    def test_partial_update_book_valid(self):
        """Test that the endpoint partial updates a book with valid data."""
        book = Book.objects.first()
        data = {"title": "Updated Book"}
        response = self.client.patch(f"{self.url}{book.pk}/", data)
        self.assertEqual(response.status_code, 200)
        book.refresh_from_db()
        self.assertEqual(book.title, data["title"])

    def test_partial_update_book_invalid(self):
        """Test that the endpoint does not partial update a book with invalid data."""
        book = Book.objects.first()
        data = {"isbn": "9783161484999-"}  # * Invalid ISBN
        response = self.client.patch(f"{self.url}{book.pk}/", data)
        self.assertEqual(response.status_code, 400)
        book.refresh_from_db()
        self.assertNotEqual(book.isbn, data["isbn"])

    def test_delete_book(self):
        """Test that the endpoint deletes a book."""
        book = Book.objects.first()
        response = self.client.delete(f"{self.url}{book.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 14)

    def test_delete_book_not_found(self):
        """Test that the endpoint does not delete a non-existent book."""
        response = self.client.delete(f"{self.url}999/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Book.objects.count(), 15)

    @staticmethod
    def _get_valid_data():
        """Returns valid data for creating or updating a book."""
        return {
            "title": "Book",
            "author": "Author",
            "published_date": timezone.now().date(),
            "isbn": "9783161484999",
            "language": "English",
        }

    def _get_invalid_data(self):
        """Returns invalid data for creating or updating a book."""
        valid_data = self._get_valid_data()
        valid_data["isbn"] = "9783161484999-"  # * Invalid ISBN
        return valid_data
