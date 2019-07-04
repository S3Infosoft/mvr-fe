from ..serializers import OTASerializer
from enquiry.models import OTA

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

OTA_URL = reverse("ota-list")


class PublicOTAAPITestCase(APITestCase):
    """Test the publically available OTA API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_always_required(self):

        res = self.client.get(OTA_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def sample_ota(name, **kwargs):
    """Create and return a sample OTA object"""

    defaults = {
        "contact_person": "Super Saiyan",
        "contact_name": "Goku",
        "contact_email": "goku@dbz.com"
    }

    if kwargs:
        defaults.update(kwargs)

    return OTA.objects.create(name=name, **defaults)


class PrivateOTAAPITestCase(APITestCase):
    """Test the OTA API available to authorized users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@s3-infosoft.com", "django123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_otas(self):

        sample_ota(name="OTA1")
        sample_ota(name='OTA2')
        sample_ota(name='OTA3')

        res = self.client.get(OTA_URL)

        otas = OTA.objects.all()
        serializer = OTASerializer(otas, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
