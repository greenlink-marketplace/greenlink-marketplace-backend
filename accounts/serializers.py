from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Analisy if is the best local for polimorfism
    username_field = "login"
    login = serializers.CharField()
    # password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")

        # Avoid mandatory field error
        attrs["username"] = login

        user = authenticate(
            request=self.context.get("request"),
            username=login,  # the backend accepts username or email
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials or inactive user."
            )

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "role": user.role,
        }
