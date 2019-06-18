from enquiry.models import OTA

from django.db import models
from django.utils.timezone import now


class Schedule(models.Model):
    property_name = models.CharField(max_length=150)
    ota_name = models.ForeignKey(OTA, on_delete=models.CASCADE)
    check_in_date = models.DateTimeField(default=now)
    check_out_date = models.DateTimeField(default=now)
    listing_position_number = models.PositiveIntegerField()
    room_category_and_rates = models.CharField(max_length=200)

    def __str__(self):
        return self.property_name + " " + self.ota_name.name
