from __future__ import annotations
import os
from django.db import models
from django.contrib.auth.models import User


def user_filename(instance: UserProfile, filename: str):
    ext = filename.split(".")[-1]
    user_id = instance.user.id
    filename = f"user_{user_id}.{ext}"
    return os.path.join("profile_pictures", filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to=user_filename, default="default.jpg")

    def __str__(self):
        return self.user.username


class Event(models.Model):
    owner = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="events"
    )
    name = models.CharField(max_length=64)
    attendees = models.ManyToManyField(UserProfile, related_name="attended_events")
    description = models.CharField(max_length=512, blank=True)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=64, blank=True)


class Calendar(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event, related_name="calendars")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    colour = models.CharField(max_length=64)


class Reminder(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    reminder_date_time = models.DateTimeField()
    message = models.CharField(max_length=256)


class Tag(models.Model):
    events = models.ManyToManyField(Event, related_name="tags")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    colour = models.CharField(max_length=64)


class Invitation(models.Model):
    sender = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="received_invitations"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    message = models.CharField(max_length=256)
