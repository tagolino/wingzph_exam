from rest_framework.routers import DefaultRouter

from .views import RideViewSet, RideEventViewSet


router = DefaultRouter()
router.register(r"events", RideEventViewSet, basename="ride-events")
router.register(r"", RideViewSet, basename="rides")

urlpatterns = router.urls
