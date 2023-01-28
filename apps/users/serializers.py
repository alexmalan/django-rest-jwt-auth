"""
User serializer.
"""
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """

    class Meta:
        """
        Meta class.
        """

        model = User
        fields = ("username", "password", "role", "deposit")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password and return it.
        """
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
