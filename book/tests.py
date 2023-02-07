from django.test import TestCase
from django.urls import reverse, resolve
from .models import Book, BookReview
from django.contrib.auth.models import User
from .views import home, book_detail


class BookModelTests(TestCase):
    """book model test class"""

    def setUp(self):
        url = reverse("book:home")
        self.response = self.client.get(url)

        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@gmail.com"
        )
        self.book = Book.objects.create(
            title="a bit of python",
            slug="a-bit-of-python",
            user=self.user,
            description="some message",
        )

    def test_create_book(self):
        """testing create book"""
        self.assertEqual(self.book.title, "a bit of python")
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.book.description, "some message")

    def test_book_home_view(self):
        """testing book home view"""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "book/home.html")
        self.assertContains(self.response, "Book4Developer")
        self.assertNotContains(self.response, "Hi there! I should not be in page")

    def test_book_home_function(self):
        """testing book home view function"""
        view = resolve("/")
        self.assertEqual(view.func.__name__, home.__name__)

    def test_book_detail_view(self):
        """testing book detail templae and function"""
        url = reverse("book:book_detail", args=[self.book.slug])
        response = self.client.get(url)
        view = resolve("/a-bit-of-python")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(view.func.__name__, book_detail.__name__)

    def test_book_upload_view_url(self):
        """testing book upload view"""
        url = reverse("book:book_upload", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_book_user_profile_url(self):
        """testing book user profile view"""
        url = reverse("book:book_user_profile", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
