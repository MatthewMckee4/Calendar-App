from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from app.forms import UserRegistrationForm, LoginForm, UserProfileForm, EventForm
from django.contrib.auth.models import User
from datetime import date
from app.models import UserProfile, Calendar, Event

APP_TEMPLATE_DIR = "app/"


def index(request):
    calendar_list = Calendar.objects
    event_list = Event.objects
    flag = True
    if request.user.is_authenticated:
        calendar_exist = Calendar.objects.filter(user=request.user).exists()
        if calendar_exist:
            flag = True
    context_dict = {
        "date": date.today(),
        "flag": flag,
        "user": request.user,
        "calendars": calendar_list,
        "events": event_list,
    }
    return render(request, f"{APP_TEMPLATE_DIR}index.html", context=context_dict)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()

            # Create the UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()

            # Log in the user
            login(request, new_user)

            return redirect("app:index")
        else:
            print("User registration failed")
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    return render(
        request,
        f"{APP_TEMPLATE_DIR}register.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("app:index"))
            else:
                try:
                    user_exists = User.objects.get(username=username)
                    messages.error(request, "Incorrect password. Please try again.")
                except User.DoesNotExist:
                    messages.error(request, "Username does not exist.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LoginForm()
    return render(request, f"{APP_TEMPLATE_DIR}login.html", {"form": form})


@login_required
def profile(request):
    context_dict = {}

    full_name_list = request.user.get_full_name().split(" ")
    context_dict["fname"] = full_name_list[0]
    context_dict["lname"] = full_name_list[1]

    userProfile = UserProfile.objects.get(user=request.user)
    if userProfile:
        context_dict["DoB"] = userProfile.date_of_birth
        context_dict["profilePhoto"] = userProfile.profile_picture_url

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userProfile
        )
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("app:profile"))
    else:
        profile_form = UserProfileForm(instance=userProfile)

    context_dict["profile_form"] = profile_form
    return render(request, f"{APP_TEMPLATE_DIR}profile.html", context=context_dict)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('app:index')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, f"{APP_TEMPLATE_DIR}password_change_form.html", {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse("app:index"))


@login_required
def calendars(request):
    return render(request, f"{APP_TEMPLATE_DIR}calendars.html")

@login_required
def events(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:events')
    else:
        form = EventForm()
    return render(request, f"{APP_TEMPLATE_DIR}events.html", {'form': form})

@login_required
def notifications(request):
    return render(request, f"{APP_TEMPLATE_DIR}notifications.html")
