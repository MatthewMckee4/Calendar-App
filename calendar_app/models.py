from django.db import models
from django.contrib.auth.models import User


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=20, default="#007bff")
    recurring = models.BooleanField(default=False)
    reminder_time = models.PositiveIntegerField(default=15)


class EventInvite(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ADMIN = "admin"
    ATTENDEE = "attendee"
    INVITE_CHOICES = [
        (ADMIN, "Admin"),
        (ATTENDEE, "Attendee"),
    ]
    invite_type = models.CharField(
        max_length=10, choices=INVITE_CHOICES, default=ATTENDEE
    )


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)


class EventTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tag = models.CharField(max_length=50)
