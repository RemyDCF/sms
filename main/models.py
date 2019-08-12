from django.db import models
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)


class Message(models.Model):
    text = models.TextField()
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    contact_is_sender = models.BooleanField()
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    media_url = models.CharField(max_length=500)
