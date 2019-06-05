from .. import models

from rest_framework import serializers


class OTASerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.OTA
        fields = "__all__"


class PartnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Partner
        fields = "__all__"


class ReviewSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Review
        fields = "__all__"
