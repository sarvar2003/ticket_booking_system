from django.urls import path

from .views import (
    ListReservationsAPIView,
    CreateReservationAPIView,
    UpdateReservationAPIView,
    PayForReservationAPIView,
    CancelReservationAPIView,
)

app_name = "reservations"

urlpatterns = [
    path('all/', ListReservationsAPIView.as_view(), name='list-reservations'),
    path('create/', CreateReservationAPIView.as_view(), name='create-reservation'),
    path('<int:pk>/update/', UpdateReservationAPIView.as_view(), name='update-reservation'),
    path('<int:pk>/pay/', PayForReservationAPIView.as_view(), name='pay-for-reservation'),
    path('<int:pk>/cancel/', CancelReservationAPIView.as_view(), name='cancel-reservation'),
]
