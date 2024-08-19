from django.test import TestCase

from ..models import Book


class BookModelTestCase(TestCase):
    """Test cases for the Book model."""

    @classmethod
    def setUpTestData(cls) -> Book:
        """Returns created Organization object for testing."""
        cls.obj = Book.objects.create(
            title="The Catcher in the Rye",
            author="J.D. Salinger",
            isbn="9780316769488",
            language="English",
        )
        cls.expected_string_representation = cls.obj.title
        return cls.obj

    def test_title_char_field(self):
        """Test that the title field is a CharField."""
        self.assertEqual(
            Book._meta.get_field("title").__class__.__name__, "CharField"
        )

    def test_title_required(self):
        """Test that the title field is required."""
        self._test_required_("title")

    def test_title_max_length(self):
        """Test that the title max length is 255."""
        self.assertEqual(Book._meta.get_field("title").max_length, 255)

    def test_author_char_field(self):
        """Test that the author field is a CharField."""
        self.assertEqual(
            Book._meta.get_field("author").__class__.__name__,
            "CharField",
        )

    def test_author_required(self):
        """Test that the author field is required."""
        self._test_required_("author")

    def test_author_max_length(self):
        """Test that the author max length is 255."""
        self.assertEqual(Book._meta.get_field("author").max_length, 255)

    def test_published_date_date_field(self):
        """Test that the published_date field is a DateField."""
        self.assertEqual(
            Book._meta.get_field("published_date").__class__.__name__,
            "DateField",
        )

    def test_published_date_not_required(self):
        """Test that the published_date field is not required."""
        self._test_not_required_("published_date")

    def test_isbn_char_field(self):
        """Test that the isbn field is a CharField."""
        self.assertEqual(
            Book._meta.get_field("isbn").__class__.__name__,
            "CharField",
        )

    def test_isbn_unique(self):
        """Test that the isbn field is unique."""
        self.assertTrue(Book._meta.get_field("isbn").unique)

    def test_isbn_required(self):
        """Test that the isbn field is required."""
        self._test_required_("isbn")

    def test_isbn_max_length(self):
        """Test that the isbn max length is 13."""
        self.assertEqual(Book._meta.get_field("isbn").max_length, 13)

    def test_pages_positive_integer_field(self):
        """Test that the pages field is a PositiveIntegerField."""
        self.assertEqual(
            Book._meta.get_field("pages").__class__.__name__,
            "PositiveIntegerField",
        )

    def test_pages_not_required(self):
        """Test that the pages field is not required."""
        self._test_not_required_("pages")

    def test_cover_url_field(self):
        """Test that the cover field is a URLField."""
        self.assertEqual(
            Book._meta.get_field("cover").__class__.__name__,
            "URLField",
        )

    def test_cover_not_required(self):
        """Test that the cover field is not required."""
        self._test_not_required_("cover")

    def test_language_char_field(self):
        """Test that the language field is a CharField."""
        self.assertEqual(
            Book._meta.get_field("language").__class__.__name__,
            "CharField",
        )

    def test_language_required(self):
        """Test that the language field is required."""
        self._test_required_("language")

    def test_language_max_length(self):
        """Test that the language max length is 50."""
        self.assertEqual(Book._meta.get_field("language").max_length, 50)

    def test_model_string_representation(self):
        """Test the model string representation by __str__."""
        self.assertEqual(str(self.obj), self.expected_string_representation)

    def _test_required_(self, field: str):
        """Test that the given field is required."""
        self.assertFalse(Book._meta.get_field(field).blank)
        self.assertFalse(Book._meta.get_field(field).null)

    def _test_not_required_(self, field: str):
        """Test that the given field is not required."""
        self.assertTrue(Book._meta.get_field(field).blank)
        self.assertTrue(Book._meta.get_field(field).null)
