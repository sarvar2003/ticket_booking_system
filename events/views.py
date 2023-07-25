from rest_framework import generics, filters
from rest_framework.response import Response

from .models import Event
from .serializers import (
    EventSerializer,
    UpdateEventSerializer,
)

# Create your views here.
class ListEventsAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CreateEventAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UpdateEventAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = UpdateEventSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        request.data['host'] = request.user

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Event updated successfully."})
        return Response(
            serializer.errors,
        )

class DeleteEventAPIView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SearchEventAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]