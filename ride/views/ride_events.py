from rest_framework import viewsets, permissions

from ..models import RideEvent
from ..serializers import RideEventSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    model = RideEvent
    queryset = RideEvent.objects.select_related("id_ride").all().order_by("-created_at")
    serializer_class = RideEventSerializer
