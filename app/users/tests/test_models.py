from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTestCase(TestCase):
    """Tests for the CustomUserManager"""

    def test_create_user_creates_a_user(self):
        """Test for create_user command using email and password"""

        params = {"email": "test@django.com", "password": "django123"}

        user = get_user_model().objects.create_user(**params)

        self.assertEqual(user.email, params["email"])
        self.assertTrue(user.check_password(params["password"]))
        self.assertIsNone(user.username)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_fails_on_invalid_parameters(self):
        """Test for create_user failure"""

        params = {"email": "test@django.com", "password": "django123"}

        User = get_user_model()
        User.objects.create_user(**params)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(params["email"], "django123")

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="django123")

    def test_create_superuser_creates_a_superuser(self):
        """Test to create a superuser successfully"""
        params = {"email": "test@django.com", "password": "django123"}

        oracle = get_user_model().objects.create_superuser(**params)

        self.assertEqual(oracle.email, params["email"])
        self.assertTrue(oracle.check_password(params["password"]))
        self.assertIsNone(oracle.username)
        self.assertTrue(oracle.is_active)
        self.assertTrue(oracle.is_staff)
        self.assertTrue(oracle.is_superuser)

    def test_create_superuser_fails_on_invalid_parameters(self):
        """Test for create_superuser failure"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email="oracle@django.com",
                password="django123",
                is_superuser=False
            )
