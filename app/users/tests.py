from django.db import IntegrityError
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

LOGIN_URL = reverse("login")
REGISTER_URL = reverse("register")


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


class LoginViewTestCase(TestCase):
    """
    Tests for the Login View
    """

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="test@django.com",
            password="django123",
        )

    def test_login_page_loads_successfull(self):

        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/login.html")

    def test_login_page_redirects_successfully(self):

        res = self.client.post(LOGIN_URL, data={
            "username": "test@django.com",
            "password": "django123",
        })

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))

    def test_redirects_already_logged_in(self):

        self.client.force_login(self.user)

        res = self.client.get(LOGIN_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))


class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_page_loads_successfully(self):

        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/register.html")

    def test_register_page_create_user(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        self.client.post(REGISTER_URL, data=params)

        user = get_user_model().objects.get(email=params["email"])

        self.assertEqual(user.first_name, params["first_name"])
        self.assertEqual(user.last_name, "")
        self.assertTrue(user.check_password(params["password1"]))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_register_page_redirects_correctly(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        res = self.client.post(REGISTER_URL, data=params)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login"))

    def test_register_page_fails_on_duplicate_user(self):

        params = {
            "email": "new_user@django.com",
            "first_name": "Abhishek",
            "password1": "testPassword",
            "password2": "testPassword",
        }

        self.client.post(REGISTER_URL, data=params)

        params.update({"first_name": "Chester", "last_name": "Bennington"})
        res = self.client.post(REGISTER_URL, data=params)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "users/register.html")
        self.assertFormError(
            res,
            "form",
            "email",
            "User with this Email address already exists."
        )

    def test_register_page_redirects_on_logged_in_user(self):

        self.client.force_login(get_user_model().objects.create_user(
            email="abhie@python.com", password="django123",
        ))

        res = self.client.get(REGISTER_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("index"))
