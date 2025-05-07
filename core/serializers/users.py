from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    role = serializers.CharField(required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
        ]


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
