# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import views, generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ResetPasswordSerializer,
    ConfirmResetPasswordSerializer,
)

from django.conf import settings

User = get_user_model()


class LoginView(views.APIView):
    """
    API View for user login.

    This view handles user authentication based on the provided credentials (username and password).
    If the user is authenticated and their account is verified, it logs them in successfully.
    If the user's account is not verified, it indicates that the user needs to verify their email.
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
            if user.is_verified:
                login(request, user)
                return Response({"detail": "User logged in successfully."})
            else:
                return Response({"detail": "User is not verified."})
        else:
            return Response(
                {"detail": "Incorrect username or password."}, status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationView(generics.GenericAPIView):
    """
    API View for user registration.

    This view handles user registration and email verification.
    Upon successful registration, it sends an activation email to the user with a verification link.
    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        """Handle user registration and email verification."""
        serialaizer = self.serializer_class(data=request.data)
        if serialaizer.is_valid():
            serialaizer.save()
            email = serialaizer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            send_mail(
                "Account Activation",
                f"http://127.0.0.1:8000/users/api/activation/confirm/{token}.",
                "from@example.com",
                [email],
                fail_silently=False,
            )
            return Response({"detail": "Please check your email"}, status=status.HTTP_201_CREATED)
        return Response(
            serialaizer.errors,
        )

    def get_tokens_for_user(self, user):
        """Generate tokens for user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationApiView(APIView):
    """
    API View for email verification (account activation).

    This view handles email verification when the user clicks the verification link.
    """

    def get(self, request, token, *args, **kwargs):
        """Handle email verification (account activation)."""
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"details": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "Your account has already been created."})
        user_obj.is_verified = True
        user_obj.save()
        return Response({"details": "Your account has been created and verified successfuly."})


class ResetPasswordApiView(generics.GenericAPIView):
    """
    API View for requesting a password reset.

    This view handles requesting a password reset by sending an email with a reset token to the user.
    """

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        """Handle password reset request."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email = user_obj.email
        send_mail(
            "Account Activation",
            f"http://127.0.0.1:8000/users/api/reset_password/confirm/{token}.",
            "from@example.com",
            [email],
            fail_silently=False,
        )
        return Response({"details": "Your password reset token has been sent successfully."})

    def get_tokens_for_user(self, user):
        """Generate tokens for user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ConfirmResetPasswordApiView(generics.GenericAPIView):
    """
    API View for confirming a password reset.

    This view handles confirming the password reset using the reset token and setting the new password.
    """

    serializer_class = ConfirmResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        """Return serializer for get request."""
        serializer = self.serializer_class()
        return Response(serializer.data)

    def put(self, request, token, *args, **kwargs):
        """Handle password reset confirmation."""
        serializer = self.serializer_class(data=request.data)
        try:
            token_dic = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token_dic.get("user_id")
        except ExpiredSignatureError:
            return Response({"detail": "Token has expired"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({"details": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        user_obj = User.objects.get(pk=user_id)
        if serializer.is_valid():
            # hash the password that the user will get
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            return Response(
                {"detail": "Your password is reset successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
