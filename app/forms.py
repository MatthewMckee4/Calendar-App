from django import forms
from django.contrib.auth.models import User
from app.models import UserProfile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def clean_confirm_password(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return confirm_password


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["date_of_birth", "profile_picture_url"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
