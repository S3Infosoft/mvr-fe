from enquiry import models as enq_models

from rest_framework import serializers

from easyaudit.models import CRUDEvent


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
        model = enq_models.OTA
        fields = "__all__"


class PartnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = enq_models.Partner
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = enq_models.Review
        fields = "__all__"
