from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class RegisterSerializer(serializers.Serializer):
    """Serializer para registro con DNI"""

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    dni = serializers.CharField(max_length=20)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VotingConfigSerializer(serializers.Serializer):
    """Serializer para el estado de la votación"""

    is_active = serializers.BooleanField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    ended_at = serializers.DateTimeField(read_only=True)
    message = serializers.CharField(read_only=True)
