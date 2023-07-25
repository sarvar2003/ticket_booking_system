from django.urls import path

from .views import (
    CreateEventAPIView,
    ListEventsAPIView,
    UpdateEventAPIView,
    DeleteEventAPIView,
    SearchEventAPIView,
)

app_name = 'events'

urlpatterns = [
    path('all/', ListEventsAPIView.as_view(), name='list-events'),
    path('create/', CreateEventAPIView.as_view(), name='create-event'),
    path('<int:pk>/update/', UpdateEventAPIView.as_view(), name='update-event'),
    path('<int:pk>/delete/', DeleteEventAPIView.as_view(), name='delete-event'),
    path('search/', SearchEventAPIView.as_view(), name='search-event'),
]
