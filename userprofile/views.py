# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from rest_framework import views, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
)


User = get_user_model()


class LoginView(views.APIView):
    """
    API View for user login.

    This view handles user authentication based on the provided credentials (username and password).
    If the user is authenticated it logs them in successfully.
    If the provided credentials are incorrect, it returns an error response.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        """Handle user login."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is not None:
            login(request, user)
            return Response({"detail": "User logged in successfully."})
        else:
            return Response(
                {"detail": "Incorrect username or password."}, status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationView(generics.GenericAPIView):
    """
    API View for user registration.

    This view handles user registration and email verification.
    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Handle user registration and email verification."""
        serialaizer = self.serializer_class(data=request.data)
        if serialaizer.is_valid():
            serialaizer.save()
            return Response({"detail": "Signed up successfully."}, status=status.HTTP_201_CREATED)
        return Response(
            serialaizer.errors,
        )


class ResetPasswordApiView(generics.GenericAPIView):
    """
    API View for confirming a password reset.

    This view handles confirming the password reset using the reset token and setting the new password.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        """Return serializer for get request."""
        serializer = self.serializer_class()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Handle password reset confirmation."""
        serializer = self.serializer_class(data=request.data)
        user_obj = request.user
        if serializer.is_valid():
            # hash the password that the user will get
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            return Response(
                {"detail": "Your password is reset successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)