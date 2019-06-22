from enquiry.models import OTA

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class Schedule(models.Model):
    STATUS = (
        ("PENDING", "Pending"),
        ("EXECUTING", "Executing"),
        ("FINISHED", "Finished"),
        ("FAILED", "Failed"),
    )

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    property_name = models.CharField(max_length=150)
    ota_name = models.ForeignKey(OTA, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField(default=now)
    check_out_date = models.DateTimeField(default=now)
    listing_position_number = models.PositiveIntegerField()
    room_category_and_rates = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=10)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.property_name + " " + self.ota_name.name
