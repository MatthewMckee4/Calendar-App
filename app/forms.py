from django import forms
from app.models import UserProfile
from django.contrib.auth.models import User
from .models import Event


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    date_of_birth = forms.DateField(required=False, label="Date of Birth")
    profile_picture = forms.ImageField(required=False, label="Profile Picture")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return confirm_password

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data.get("username"),
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password"),
            first_name=self.cleaned_data.get("first_name"),
            last_name=self.cleaned_data.get("last_name"),
        )
        user_profile.user = user
        user_profile.date_of_birth = self.cleaned_data.get("date_of_birth")
        profile_picture = self.cleaned_data.get("profile_picture")
        if profile_picture:
            user_profile.profile_picture = profile_picture
        else:
            user_profile.profile_picture = None

        if commit:
            user.save()
            user_profile.save()

        return user_profile


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
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(EventForm, self).__init__(*args, **kwargs)
        if self.user:
            del self.fields["owner"]
            self.instance.owner = self.user

    attendees = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.all())

    location_latitude = forms.FloatField()
    location_longitude = forms.FloatField()
    start_date_time = forms.DateTimeField()
    end_date_time = forms.DateTimeField()
    description = forms.CharField(max_length=512, required=False)

    class Meta:
        model = Event
        fields = "__all__"
