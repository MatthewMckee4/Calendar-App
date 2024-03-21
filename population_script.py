import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calendar_app.settings")

import django

django.setup()

from app.models import UserProfile, Event, Calendar, Reminder, Tag, Invitation
from django.utils import timezone
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

names = [
    ("Alice", "Smith"),
    ("Bob", "Jones"),
    ("Charlie", "Brown"),
    ("David", "Williams"),
    ("Eve", "Taylor"),
    ("Frank", "Wilson"),
    ("Grace", "Evans"),
    ("Harry", "Thomas"),
    ("Ivy", "Harris"),
    ("Jack", "Martin"),
]


def create_users(num_users):
    for i in range(num_users):
        username = f"user_{i}"
        email = f"user{i}@example.com"
        password = "password123"
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=names[i][0],
            last_name=names[i][1],
        )

        image_data = open(f"media/profile_pictures/user_{i}.jpg", "rb").read()
        profile_picture = SimpleUploadedFile(
            f"user_{i}.jpg", image_data, content_type="image/jpeg"
        )

        user_profile = UserProfile.objects.create(
            user=user, date_of_birth=datetime.now(), profile_picture=profile_picture
        )


def create_events(num_events):
    users = UserProfile.objects.all()
    for i in range(num_events):
        owner = random.choice(users)
        start_datetime = timezone.now() + timedelta(days=i)
        end_datetime = start_datetime + timedelta(hours=1)
        event = Event.objects.create(
            owner=owner,
            name=f"Event {i}",
            description=f"This is event {i}",
            start_date_time=start_datetime,
            end_date_time=end_datetime,
            location_latitude=random.uniform(55.5, 56.5),
            location_longitude=random.uniform(-4.5, -3.5),
        )
        event.save()


def create_calendars(num_calendars):
    users = UserProfile.objects.all()
    for i in range(num_calendars):
        user = random.choice(users)
        Calendar.objects.create(
            user=user,
            name=f"Calendar {i}",
            description=f"This is calendar {i}",
            colour="blue",
        )


def create_reminders(num_reminders):
    users = UserProfile.objects.all()
    events = Event.objects.all()
    for i in range(num_reminders):
        user = random.choice(users)
        event = random.choice(events)
        Reminder.objects.create(
            user=user,
            event=event,
            reminder_date_time=event.start_date_time - timedelta(hours=1),
            message=f"Reminder for event {event.name}",
        )


def create_tags(num_tags):
    events = Event.objects.all()
    for i in range(num_tags):
        event = random.choice(events)
        Tag.objects.create(
            name=f"Tag {i}", description=f"This is tag {i}", colour="green"
        )
        event.tags.add(Tag.objects.last())
        event.save()


def create_invitations(num_invitations):
    users = UserProfile.objects.all()
    events = Event.objects.all()
    for i in range(num_invitations):
        sender = random.choice(users)
        receiver = random.choice(users)
        event = random.choice(events)
        status = random.choice(["pending", "accepted", "declined"])
        Invitation.objects.create(
            sender=sender,
            receiver=receiver,
            event=event,
            status=status,
            message=f"Invitation to event {event.name}",
        )


if __name__ == "__main__":
    create_users(10)
    create_events(20)
    create_calendars(5)
    create_reminders(15)
    create_tags(5)
    create_invitations(15)
