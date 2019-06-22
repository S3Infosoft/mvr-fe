from django.db import models


class OTA(models.Model):
    name = models.CharField(max_length=150)
    registration = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    contact_person = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150)
    contact_email = models.EmailField()

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.name


class Partner(models.Model):
    PARTNERS = (
        ("TRAVEL_AGENT", "Travel Agent"),
        ("DIGITAL_PARTNER", "Digital Partner"),
        ("CORPORATE", "Corporate"),
        ("TOUR_ORGANISER", "Tour Organiser"),
    )
    name = models.CharField(max_length=150)
    partner_type = models.CharField(choices=PARTNERS, max_length=30)
    contact_person = models.CharField(max_length=150)
    contact_name = models.CharField(max_length=150)
    contact_email = models.EmailField()

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.name


class Review(models.Model):
    RATINGS = (
        (1, "Worst"),
        (2, "Poor"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent"),
    )
    headline = models.CharField(max_length=250)
    source = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.FloatField(choices=RATINGS)
    description = models.TextField()
    action = models.TextField()

    class Meta:
        ordering = "-id",

    def __str__(self):
        return self.headline
