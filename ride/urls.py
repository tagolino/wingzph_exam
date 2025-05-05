from rest_framework.routers import DefaultRouter

from .views import RideViewSet


router = DefaultRouter()
router.register(r"rides", RideViewSet, basename="rides")

urlpatterns = router.urls
