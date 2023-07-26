from rest_framework import serializers
from rest_framework.response import Response

from .models import Reservation
from events.models import Event


class CustomBaseSerializer(serializers.BaseSerializer):


    def validate(self, attrs):
        number_of_tickets = attrs.get('number_of_tickets')
        event = attrs.get('event')
        status = attrs.get('status')


        # Check if the user is not booking 0 tickets
        if number_of_tickets <= 0:
            raise serializers.ValidationError({"detail":"You should book at leats 1 ticket in order to complete reservation."})

        # Check if there are enough seats available for reservation
        if event.number_of_seats < number_of_tickets:
            raise serializers.ValidationError({"detail":"There aren't enough seats for reservation."})
        
        # Check if the reservation is not canceled or confirmed 
        # (for updating reservation only pending reservation are accepted)
        if status == "Confirmed":
            raise serializers.ValidationError({"detail":"You cannot update confirmed or canceled reservations."})        

        return super().validate(attrs)


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer class for Reservation model"""

    class Meta:
        model = Reservation
        fields = ( "id", "event", "number_of_tickets", "guest", "status")
        read_only_fields = ("id", "guest", "status")
    

    def create(self, validated_data):
        guest = self.context['request'].user
        validated_data['guest'] = guest

        return super().create(validated_data)


class ReservationUpdateSerializer(serializers.ModelSerializer):
    """Serializer class for updating reservation"""

    class Meta:
        model = Reservation
        fields = ( "id", "event", "number_of_tickets", "guest", "status")
        read_only_fields = ("id", "guest", "status")

    
    def update(self, instance, validated_data):
        guest = self.context['request'].user
        validated_data['guest'] = guest

        return super().update(instance, validated_data) 




class ReservationPaymentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Reservation
        fields = ("id", "event", "number_of_tickets", "status")
        read_only_fields = ("id", "event", "number_of_tickets", "status")