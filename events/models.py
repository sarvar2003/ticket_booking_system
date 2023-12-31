from django.db import models
from django.contrib.auth import get_user_model

from .choices import TOPICCHOICES, CURRENCIES

User = get_user_model()

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, choices=TOPICCHOICES)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    place = models.CharField(max_length=250)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, blank=True, related_name="Guests")
    number_of_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCIES, default="UZS")
    thumbnail = models.FileField(upload_to=None, max_length=100)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    