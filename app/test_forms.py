import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "calendar_app.settings")

import django

django.setup()


from django.test import TestCase
from django.contrib.auth.models import User
from app.models import UserProfile, Calendar
from .forms import (
    UserRegistrationForm,
    UserProfileForm,
    LoginForm,
    EventForm,
    CalendarForm,
    AddToCalendarForm,
)


class FormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.calendar = Calendar.objects.create(
            name="test calendar", user=self.user_profile
        )

    def test_UserRegistrationForm_valid_data(self):
        form_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword",
            "confirm_password": "newpassword",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_UserRegistrationForm_invalid_data(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "confirm_password": "wrongpassword",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_UserProfileForm_valid_data(self):
        form_data = {
            "username": "updatedusername",
            "first_name": "Updated",
            "last_name": "User",
            "email": "updated@example.com",
            "date_of_birth": "2000-01-01",
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertTrue(form.is_valid())

    def test_UserProfileForm_invalid_data(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "date_of_birth": "invalid_date",
        }
        form = UserProfileForm(data=form_data, instance=self.user_profile)
        self.assertFalse(form.is_valid())

    def test_LoginForm_valid_data(self):
        form_data = {
            "username": "testuser",
            "password": "password",
        }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_EventForm_valid_data(self):
        form_data = {
            "name": "Test Event",
            "attendees": [self.user_profile.pk],
            "location_latitude": 0,
            "location_longitude": 0,
            "start_date_time": "2024-03-22T12:00",
            "end_date_time": "2024-03-22T13:00",
        }
        form = EventForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_EventForm_invalid_data(self):
        form_data = {
            "name": "",
            "attendees": [],
            "location_latitude": 0,
            "location_longitude": 0,
            "start_date_time": "",
            "end_date_time": "",
        }
        form = EventForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_CalendarForm_valid_data(self):
        form_data = {
            "name": "Test Calendar",
            "description": "Test Description",
            "colour": "#000000",
        }
        form = CalendarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_CalendarForm_invalid_data(self):
        form_data = {
            "name": "",
            "description": "Test Description",
            "colour": "#000000",
        }
        form = CalendarForm(data=form_data)
        self.assertFalse(form.is_valid())

        self.assertFalse(form.is_valid())
