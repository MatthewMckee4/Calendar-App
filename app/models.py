from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    profile_picture_url = models.CharField(max_length=128)

    def __str__(self):
        return self.user.username


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    events = models.ManyToManyField("Event", related_name="calendars")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    colour = models.CharField(max_length=64)


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    reminder_date_time = models.DateTimeField()
    message = models.CharField(max_length=256)


class Tag(models.Model):
    events = models.ManyToManyField("Event", related_name="tags")
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    colour = models.CharField(max_length=64)


class Event(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_events"
    )
    attendees = models.ManyToManyField(User, related_name="attended_events")
    description = models.CharField(max_length=512)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    recurring = models.BooleanField(default=False)
    recurring_frequency = models.CharField(max_length=64, blank=True)


class Invitation(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invitations"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_invitations"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    message = models.CharField(max_length=256)
