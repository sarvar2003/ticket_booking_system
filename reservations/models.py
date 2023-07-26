from django.db import models
from django.contrib.auth import get_user_model

from .choices import RESERVATION_STATUS

User = get_user_model()

# Create your models here.
class Reservation(models.Model):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="Guest")
    number_of_tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=RESERVATION_STATUS, default="Pending")


    def get_total_price(self, *args, **kwargs):
        price = self.event.ticket_price

        return price * self.number_of_tickets