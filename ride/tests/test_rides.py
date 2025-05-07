import pytest

from django.utils import timezone
from django.test.utils import CaptureQueriesContext
from django.db import connection
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
        status="pickup",
        pickup_time=timezone.now(),
    )

@pytest.fixture
def ride_event(ride):
    return RideEvent.objects.create(
        id_ride=ride,
        description="test",
    )

@pytest.mark.django_db
class TestRideAPI:
    def test_create_ride(self, auth_client, rider, driver):
        payload = {
            "driver_id": driver.id,
            "rider_id": rider.id,
            "status": "pickup",
            "pickup_latitude": 222.123,
            "pickup_longitude": 33.321,
            "dropoff_latitude": 44.123,
            "dropoff_longitude": 66.11,
            "pickup_time": f"{timezone.now().date().isoformat()} 00:00:00",
        }
        response = auth_client.post("/api/rides/", payload)
        assert response.status_code == 201

    def test_list_rides_with_query_count(self, auth_client, ride):
        with CaptureQueriesContext(connection) as queries:
            response = auth_client.get("/api/rides/")
            assert response.status_code == 200
            assert "todays_ride_events" in response.data["results"][0]
        assert len(queries) <= 3  # 2 main queries + 1 for pagination count

    def test_retrieve_ride(self, auth_client, ride):
        response = auth_client.get(f"/api/rides/{ride.id}/")
        assert response.status_code == 200

    def test_update_ride(self, auth_client, ride):
        response = auth_client.patch(f"/api/rides/{ride.id}/", {"status": "dropoff"})
        assert response.status_code == 200

    def test_delete_ride(self, auth_client, ride):
        response = auth_client.delete(f"/api/rides/{ride.id}/")
        assert response.status_code == 204
        assert not Ride.objects.filter(id=ride.id).exists()
