from datetime import timedelta
from django.db.models import Prefetch
from django.db.models.expressions import RawSQL
from django.utils.timezone import now
from rest_framework import viewsets

from ..filters import RideFilter
from ..models import Ride, RideEvent
from ..serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    model = Ride
    queryset = Ride.objects.select_related("id_rider", "id_driver").all().order_by("-pickup_time")
    serializer_class = RideSerializer
    filterset_class = RideFilter
    ordering_fields = ["pickup_time"]
    ordering = ["pickup_time"]

    def get_queryset(self):
        self.queryset = super().get_queryset()

        last_24_hours = now() - timedelta(hours=24)

        recent_events_qs = (
            RideEvent.objects.filter(
                created_at__gte=last_24_hours
            )
            .only("id", "id_ride", "description", "created_at")
        )

        self.queryset = (
            self.queryset.prefetch_related(
                Prefetch("events", queryset=recent_events_qs, to_attr="todays_ride_events")
            )
        )

        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")

        if lat and lng:
            lat = float(lat)
            lng = float(lng)

            # Simple Haversine formula approximation in SQL
            self.queryset = self.queryset.annotate(
                distance=RawSQL(
                    "SQRT(POW(pickup_latitude - %s, 2) + POW(pickup_longitude - %s, 2))",
                    (lat, lng)
                )
            ).order_by("distance")

        return self.queryset
