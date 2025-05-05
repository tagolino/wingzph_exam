from rest_framework import serializers

from ..models import Ride
from core.models import User


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class RideSerializer(serializers.ModelSerializer):
    id_rider = UserBriefSerializer(read_only=True)
    id_driver = UserBriefSerializer(read_only=True)

    id_rider_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="rider"),
        source="id_rider",
        write_only=True
    )
    id_driver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role="driver"),
        source="id_driver",
        write_only=True
    )

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
            "id_rider",
            "id_driver",
            "id_rider_id",
            "id_driver_id",
        ]
