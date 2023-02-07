from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import sing_up, sing_in


class UserAccountTests(TestCase):
    """user account testing class"""

    def test_create_user(self):
        """testing normal user account"""
        user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@gmail.com"
        )

        self.assertEqual(user.email, "test@gmail.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """testing super user account"""
        admin_user = User.objects.create_superuser(
            username="superadmin", password="testpass123", email="superadmin@gmail.com"
        )

        self.assertEqual(admin_user.email, "superadmin@gmail.com")
        self.assertEqual(admin_user.username, "superadmin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class RegisterPageTests(TestCase):
    """user register test class"""

    def setUp(self):
        """setting up"""
        url = reverse("accounts:register")
        self.response = self.client.get(url)

    def test_singup_template(self):
        """register template testing"""
        self.assertTemplateUsed(self.response, "accounts/register.html")
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, "Register")
        self.assertNotContains(self.response, "Hi there! I should not be in the page.")

    def test_singup_view(self):
        """testing singup view function"""
        view = resolve("/accounts/register")
        self.assertEqual(view.func.__name__, sing_up.__name__)


class LoginPageTests(TestCase):
    """user login test class"""

    def setUp(self):
        url = reverse("accounts:login")
        self.response = self.client.get(url)

    def test_login_template(self):
        """login template testing"""
        self.assertTemplateUsed(self.response, "accounts/login.html")
        self.assertEqual(self.response.status_code, 200)
        self.assertNotContains(self.response, "Hi there! I should not be in login page")
        self.assertContains(self.response, "Login")

    def test_login_view(self):
        """testing login_view function"""
        view = resolve("/accounts/login")
        self.assertEqual(view.func.__name__, sing_in.__name__)
