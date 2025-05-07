from rest_framework import serializers

from ..models import RideEvent


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ["id", "id_ride", "description", "created_at"]
        read_only_fields = ["created_at"]
