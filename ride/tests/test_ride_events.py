import pytest

from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient

from ride.models import Ride, RideEvent
from core.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(
        username="admin1",
        email="admin@test.com",
        password="adminpass",
        role="admin",
        is_staff=True
    )
    return user

@pytest.fixture
def rider(db):
    return User.objects.create_user(
        username="testrider",
        email="rider@test.com",
        password="testpass123",
        role="rider"
    )

@pytest.fixture
def driver(db):
    return User.objects.create_user(
        username="testdriver",
        email="drive@test.com",
        password="testpass123",
        role="driver"
    )

@pytest.fixture
def auth_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def ride(rider, driver):
    return Ride.objects.create(
        id_driver=driver,
        id_rider=rider,
        pickup_latitude=37.77383194906347,
        pickup_longitude=-122.42817972066156,
        dropoff_latitude=37.79082356183913,
        dropoff_longitude=-122.4129359107444,
        status="scheduled",
        pickup_time=timezone.now(),
    )

@pytest.fixture
def ride_event(ride):
    return RideEvent.objects.create(
        id_ride=ride,
        description="test",
    )

@pytest.mark.django_db
class TestRideEventAPI:
    def test_create_ride_event(self, auth_client, ride):
        payload = {
            "id_ride": ride.id,
            "description": "test",
        }
        response = auth_client.post("/api/rides/events/", payload)
        assert response.status_code == 201

    def test_list_ride_events(self, auth_client):
        response = auth_client.get("/api/rides/events/")
        assert response.status_code == 200
        assert isinstance(response.data["results"], list)

    def test_retrieve_ride_event(self, auth_client, ride_event):
        response = auth_client.get(f"/api/rides/events/{ride_event.id}/")
        assert response.status_code == 200

    def test_update_ride_event(self, auth_client, ride_event):
        new_time = timezone.now() + timedelta(hours=1)
        response = auth_client.patch(f"/api/rides/events/{ride_event.id}/", {"timestamp": new_time.isoformat()})
        assert response.status_code == 200

    def test_delete_ride_event(self, auth_client, ride_event):
        response = auth_client.delete(f"/api/rides/events/{ride_event.id}/")
        assert response.status_code == 204
        assert not RideEvent.objects.filter(id=ride_event.id).exists()
