from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

OTA_LIST_URL = reverse("enquiry:ota")
PARTNER_LIST_URL = reverse("enquiry:partner")
REVIEW_LIST_URL = reverse("enquiry:review")


class OTAListViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(OTA_LIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login") + "?next=" + OTA_LIST_URL)

    def test_page_loads_for_authenticated_users(self):

        user = get_user_model().objects.create_user("test@s3-infosoft.com", "django123")
        self.client.force_login(user)

        res = self.client.get(OTA_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/ota_list.html")


class PartnerListViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(PARTNER_LIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login") + "?next=" + PARTNER_LIST_URL)

    def test_page_loads_for_authenticated_users(self):

        user = get_user_model().objects.create_user("test@s3-infosoft.com", "django123")
        self.client.force_login(user)

        res = self.client.get(PARTNER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/partner_list.html")


class ReviewListViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_to_login_for_unauthenticated_user(self):

        res = self.client.get(REVIEW_LIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("login") + "?next=" + REVIEW_LIST_URL)

    def test_page_loads_for_authenticated_users(self):

        user = get_user_model().objects.create_user("test@s3-infosoft.com", "django123")
        self.client.force_login(user)

        res = self.client.get(REVIEW_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "enquiry/review_list.html")
