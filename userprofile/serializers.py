from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


CustomUser = get_user_model()

class LoginSerializer(serializers.ModelSerializer):
    """Serializer for user login data."""

    class Meta:
        model = CustomUser
        fields = ("username", "password")


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration data."""

    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "password1",
        )

    def validate(self, attrs):
        """Validate registration data."""
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")
        password1 = attrs.get("password1")
        dob = attrs.get("dob")
        gender = attrs.get("gender")
        # Check if all fields are provided
        if not all([first_name, last_name, email, username, password, password1]):
            raise serializers.ValidationError({"detail": "Please fill in all the fields."})
        # Check if the username is already taken
        if UserProfile.objects.filter(username=username):
            raise serializers.ValidationError({"detail": "This username is already taken."})
        # Check if the passwords match
        if password != password1:
            raise serializers.ValidationError({"detail": "passwords do not match"})

        # Validate password using password validation
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        """Create a new user with validated data."""
        validated_data.pop("password1", None)
        return CustomUser.objects.create_user(**validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting user's password."""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """Validate email address for password reset."""
        email = attrs.get("email")
        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"details": "user does not exist"})
        # Check if the user's email is verified (account activated) before proceeding with password reset
        if not user_obj.is_verified:
            raise serializers.ValidationError(
                {
                    "detail": "we sent you a verification mail. Please verify your email address first."
                }
            )

        attrs["user"] = user_obj
        return super().validate(attrs)


class ConfirmResetPasswordSerializer(serializers.Serializer):
    """Serializer for confirming user's password reset."""

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """Validate the new password for password reset confirmation."""
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "New passwords do not match"})
        # Validate the new password using password validation
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)
