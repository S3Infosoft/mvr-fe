from . import serializers, mixins
from .. import models

from easyaudit.models import CRUDEvent
from rest_framework.generics import ListAPIView


class ActivityListAPIView(ListAPIView):
    serializer_class = serializers.CRUDEventSerializer
    queryset = CRUDEvent.objects.all()


class OTAViewset(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.OTASerializer
    queryset = models.OTA.objects.all()


class PartnerSerializer(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.PartnerSerializer
    queryset = models.Partner.objects.all()


class ReviewSerializer(mixins.CRUDModelViewSetMixin):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
