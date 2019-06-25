from .. import models

from easyaudit.models import CRUDEvent
from rest_framework import serializers


class CRUDEventSerializer(serializers.ModelSerializer):
    event_type = serializers.SerializerMethodField()
    content_type = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = CRUDEvent
        exclude = ("object_id", "user_pk_as_string",
                   "object_json_repr")

    @staticmethod
    def get_event_type(obj):
        return obj.get_event_type_display()


class OTASerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OTA
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Partner
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = "__all__"
