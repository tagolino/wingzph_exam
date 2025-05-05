from rest_framework import viewsets, permissions

from ..models import Ride
from ..serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    model = Ride
    queryset = Ride.objects.select_related("id_rider", "id_driver").all()
    serializer_class = RideSerializer
