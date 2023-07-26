from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from events.models import Event
from .models import Reservation
from .serializers import ReservationSerializer, ReservationPaymentSerializer, ReservationUpdateSerializer

# Create your views here.
class ListReservationsAPIView(generics.ListAPIView):
    """API view to list all created reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(guest=self.request.user)

    


class CreateReservationAPIView(generics.CreateAPIView):
    """API view to create a reservation"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class UpdateReservationAPIView(generics.UpdateAPIView, LoginRequiredMixin):
    """API view to update reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(guest=self.request.user)

class PayForReservationAPIView(generics.UpdateAPIView):
    """API view to pay for reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(guest=self.request.user)

    def update(self, request, *args, **kwargs):
        reservation_id = kwargs['pk']
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        event = reservation.event
        total_price = reservation.get_total_price()
        
        if event.number_of_seats < reservation.number_of_tickets:
            raise ValidationError({"detail":"There aren't enough seats for reservation."})
        
        if reservation.status == "Confirmed":
            raise ValidationError({"detail":"You have already paid for the tickets and your reservation is confirmed."})

        reservation.status = "Confirmed"
        event.number_of_seats -= reservation.number_of_tickets

        reservation.save()
        event.save()

        return Response({"message":f"{total_price} {event.currency} has been withdrawn from your bank account. Your reservation is now confirmed."})


class CancelReservationAPIView(generics.DestroyAPIView):
    """API view to cancel reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(guest=self.request.user)
