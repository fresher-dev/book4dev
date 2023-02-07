from django.test import TestCase
from django.urls import resolve, reverse
from .models import Blog, BlogComment
from django.contrib.auth.models import User
from .views import home, post_detail


class BlogModelTests(TestCase):
    """Blog test class"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@gmail.com"
        )
        self.post = Blog.objects.create(
            title="a bit of python",
            user=self.user,
            slug="a-bit-of-python",
            body="some message",
            status=0,
        )

    def test_create_blog_post(self):
        """testing create blog post"""
        self.assertEqual(self.post.title, "a bit of python")
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.body, "some message")
        self.assertEqual(self.post.status, 0)

    def test_blog_comment(self):
        """testing blog comment"""
        comment = BlogComment(
            user=self.user,
            email=self.user.email,
            body="a blog comment",
            blog=self.post,
        )

        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.email, self.user.email)
        self.assertEqual(comment.body, "a blog comment")
        self.assertEqual(comment.blog, self.post)


class BlogViewTests(TestCase):
    """blog view test class"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@gmail.com"
        )
        self.post = Blog.objects.create(
            title="a bit of python",
            user=self.user,
            slug="a-bit-of-python",
            body="some message",
            status=0,
        )

    def test_blog_home_view(self):
        """testing blog home view"""
        view = resolve("/blog/")
        self.assertEqual(view.func.__name__, home.__name__)

    def test_blog_detail_view(self):
        """testing blog detail view"""
        view = resolve("/blog/a-bit-of-python")
        self.assertEqual(view.func.__name__, post_detail.__name__)
