import pytest

from rest_framework.test import APIClient

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
def auth_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.mark.django_db
class TestUserAPI:
    def test_create_user(self, auth_client):
        payload = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "testpass123",
            "role": "rider",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "1234567890"
        }
        response = auth_client.post("/api/users/", payload)
        assert response.status_code == 201
        assert response.data["username"] == "newuser"

    def test_list_users(self, auth_client):
        response = auth_client.get("/api/users/")
        assert response.status_code == 200
        assert isinstance(response.data["results"], list)

    def test_retrieve_user(self, auth_client, admin_user):
        response = auth_client.get(f"/api/users/{admin_user.id}/")
        assert response.status_code == 200
        assert response.data["username"] == admin_user.username

    def test_update_user(self, auth_client, admin_user):
        response = auth_client.patch(f"/api/users/{admin_user.id}/", {"first_name": "Updated"})
        assert response.status_code == 200
        assert response.data["first_name"] == "Updated"

    def test_delete_user(self, auth_client):
        user = User.objects.create_user(username="tempuser", password="pass", role="driver")
        response = auth_client.delete(f"/api/users/{user.id}/")
        assert response.status_code == 204
        assert not User.objects.filter(id=user.id).exists()
