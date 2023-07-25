from django.urls import path

from .views import (
    LoginView,
    RegistrationView,
    ResetPasswordApiView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("reset_password/", ResetPasswordApiView.as_view(), name="reset_password"),
]
