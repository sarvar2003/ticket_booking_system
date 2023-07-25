from rest_framework import serializers
from datetime import datetime, timezone

from .models import Event

class CustomBaseSerializer(serializers.Serializer):
    """Custom base serializer to override validate method and use it accross all serializers"""

    def validate(self, attrs):
        name = attrs.get('name')
        topic = attrs.get('topic')
        date = attrs.get('date')
        place = attrs.get('place')
        number_of_seats = attrs.get('number_of_seats')
        ticket_price = attrs.get('ticket_price')
        currency = attrs.get('currency')
        thumbnail = attrs.get('thumbnail')
        description = attrs.get('description')
        
        # Check if all fields are provided
        if not all([name, topic, date, place, number_of_seats, thumbnail, description]):
            raise serializers.ValidationError({"detail": "Please fill in all the fields."})

        # Check if the date for the event is in the future
        curr_datetime = datetime.now(timezone.utc)
        if date < curr_datetime:
            raise serializers.ValidationError({"detail":"You cannot create an event in the past."})

        # Check if the price for the ticket is positive
        if ticket_price < 0:
            raise serializers.ValidationError({"detail":"Price of a ticket must be postive."})


        return super().validate(attrs)


class EventSerializer(serializers.ModelSerializer, CustomBaseSerializer):
   
    class Meta:   
        model = Event
        fields = ('id', 'name', 'topic', 'date', 'place', 'number_of_seats', 'ticket_price', 'currency', 'host', 'guests', 'thumbnail', 'description')
        read_only_fields = ('host', 'id', 'guests')

    
    
    def create(self, validated_data):
        """Create event with the validated data"""
        host =  self.context['request'].user
        validated_data['host'] = host
        return Event.objects.create(**validated_data)


class UpdateEventSerializer(serializers.ModelSerializer, CustomBaseSerializer):


    class Meta:
        model = Event
        fields = ('name', 'topic', 'date', 'place', 'number_of_seats', 'ticket_price', 'currency', 'thumbnail', 'description')
            