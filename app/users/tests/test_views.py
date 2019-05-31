from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

LOGIN_URL = reverse("login")
REGISTER_URL = reverse("register")


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


class IndexViewTestCase(TestCase):
    """"Test for the index page view"""

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get("/")

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, LOGIN_URL+"?next=/")

    def test_page_access_to_authenticated_users(self):

        user = get_user_model().objects.create_user("test@django.com", "django123")
        self.client.force_login(user)

        res = self.client.get("/")

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "index.html")
