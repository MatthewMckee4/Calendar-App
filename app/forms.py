import os
from django import forms
from django.contrib.auth.models import User
from app.models import UserProfile
from .models import Event


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
        ]

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return confirm_password


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    date_of_birth = forms.DateField(required=False, label="Date of Birth")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "profile_picture",
        ]

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = user_profile.user
        user.username = self.cleaned_data.get("username")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.date_of_birth = self.cleaned_data.get("date_of_birth")
        profile_picture = self.cleaned_data.get("profile_picture")
        if profile_picture:
            user.profile_picture = profile_picture
        else:
            user.profile_picture = None

        if commit:
            user_profile.save()
            user.save()

        return user_profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "owner",
            "attendees",
            "description",
            "start_date_time",
            "end_date_time",
            "location_latitude",
            "location_longitude",
            "recurring",
            "recurring_frequency",
        ]
        widgets = {
            "owner": forms.Select(),
            "attendees": forms.SelectMultiple(),
            "start_date_time": forms.DateTimeInput(),
            "end_date_time": forms.DateTimeInput(),
            "description": forms.Textarea(
                attrs={"label": "Event Name", "cols": 20, "rows": 1}
            ),
            "location_latitude": forms.TextInput(
                attrs={"label": "Latitude", "cols": 20, "rows": 1}
            ),
            "location_longitude": forms.TextInput(
                attrs={"label": "Longitude", "cols": 20, "rows": 1}
            ),
        }
