from ..serializers import PartnerSerializer
from enquiry.models import Partner

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

PARTNER_URL = reverse("partner-list")


class PublicPartnerAPITestCase(TestCase):
    """Test the publically available Partner API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_always_required(self):

        res = self.client.get(PARTNER_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def sample_partner(name, **kwargs):
    """Create and return a sample Partner object"""

    defaults = {
        "partner_type": "TRAVEL_AGENT",
        "contact_person": "Super Saiyan",
        "contact_name": "Goku",
        "contact_email": "goku@dbz.com"
    }

    if kwargs:
        defaults.update(kwargs)

    return Partner.objects.create(name=name, **defaults)


class PrivatePartnerAPITestCase(TestCase):
    """Test the Partner API available to authorized users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("test@s3-infosoft.com", "django123")
        self.client.force_authenticate(self.user)

    def test_retrieve_all_partners(self):

        sample_partner(name="Partner1")
        sample_partner(name='Partner2')
        sample_partner(name='Partner3')

        res = self.client.get(PARTNER_URL)

        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
