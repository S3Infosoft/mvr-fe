from . import serializers
from .. import models

from rest_framework import viewsets


class OTAViewset(viewsets.ModelViewSet):
    serializer_class = serializers.OTASerializer
    queryset = models.OTA.objects.all()


class PartnerSerializer(viewsets.ModelViewSet):
    serializer_class = serializers.PartnerSerializer
    queryset = models.Partner.objects.all()


class ReviewSerializer(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    queryset = models.Review.objects.all()
