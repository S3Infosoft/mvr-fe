from ..serializers import ReviewSerializer
from enquiry.models import Review

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

REVIEW_URL = reverse("review-list")


class PublicReviewAPITestCase(TestCase):
    """Test the publically available Review API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_always_required(self):

        res = self.client.get(REVIEW_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


def sample_review(headline, **kwargs):
    """Create and return a sample Review object"""

    defaults = {
        "source": "Khhoofiya",
        "rating": 4,
        "description": "Its just a test, no need.",
        "action": "packup",
    }

    if kwargs:
        defaults.update(kwargs)

    return Review.objects.create(headline=headline, **defaults)


class PrivateReviewAPITestCase(TestCase):
    """Test the Review API available to authorized users"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@s3-infosoft.com", "django123"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_all_reviews(self):

        sample_review(headline="REVIEW1")
        sample_review(headline='REVIEW2')
        sample_review(headline='REVIEW3')

        res = self.client.get(REVIEW_URL)

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
