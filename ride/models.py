from django.db import models
from django.conf import settings


class Ride(models.Model):
    STATUS_CHOICES = (
        ("en-route", "En Route"),
        ("pickup", "Pickup"),
        ("dropoff", "Dropoff"),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id_rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides_as_rider"
    )
    id_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rides_as_driver"
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride #{self.pk} - {self.status}"

class RideEvent(models.Model):
    id_ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name="events"
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event for Ride #{self.id_ride_id} at {self.created_at}"
