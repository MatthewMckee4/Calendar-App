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
        fields = ["username", "email", "password", "confirm_password", "first_name", "last_name"]

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return confirm_password


class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        label="Date of Birth", widget=forms.DateInput(attrs={"type": "date"})
    )
    profile_picture = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = UserProfile
        fields = ["date_of_birth", "profile_picture"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['owner', 'attendees', 'description', 'start_date_time', 'end_date_time', 'location_latitude', 'location_longitude', 'recurring', 'recurring_frequency']
        widgets = {
            'owner': forms.Select(),
            'attendees': forms.SelectMultiple(),
            'start_date_time': forms.DateTimeInput(),
            'end_date_time': forms.DateTimeInput(),
        }