from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    LoginView,
    RegistrationView,
    ActivationApiView,
    ResetPasswordApiView,
    ConfirmResetPasswordApiView,
)

urlpatterns = [
    path("api/login/", LoginView.as_view(), name="login"),
    path("api/registration/", RegistrationView.as_view(), name="registration"),
    path("api/activation/confirm/<str:token>", ActivationApiView.as_view(), name="activation"),
    path("api/reset_password/", ResetPasswordApiView.as_view(), name="reset_password"),
    path(
        "api/reset_password/confirm/<str:token>",
        ConfirmResetPasswordApiView.as_view(),
        name="confirm_reset_password",
    ),
]
