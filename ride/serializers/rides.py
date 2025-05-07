from rest_framework import serializers

from ..models import Ride, RideEvent
from core.models import User
from core.serializers import UserShortSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id", "description", "created_at"]


class RideSerializer(serializers.ModelSerializer):
    rider = UserShortSerializer(source="id_rider", required=False)
    driver = UserShortSerializer(source="id_driver", required=False)

    rider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="rider"),
        source="id_rider",
        write_only=True
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="driver"),
        source="id_driver",
        write_only=True
    )

    todays_ride_events = RideEventSerializer(many=True, read_only=True)

    class Meta:
        model = Ride
        fields = [
            "id",
            "status",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "rider",
            "driver",
            "rider_id",
            "driver_id",
            "todays_ride_events",
        ]
