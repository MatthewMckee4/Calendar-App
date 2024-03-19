from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from app.forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from app.forms import UserRegistrationForm, LoginForm, UserProfileForm, EventForm
from django.contrib.auth.models import User
from app.models import UserProfile, Calendar, Event
from .models import Event
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone

APP_TEMPLATE_DIR = "app/"


def index(request):
    calendar_list = Calendar.objects.all()
    event_list = Event.objects.all().order_by("start_date_time")

    today_date = date.today()
    monday = today_date - timedelta(days=today_date.weekday())
    tuesday = monday + timedelta(days=1)
    wednesday = monday + timedelta(days=2)
    thursday = monday + timedelta(days=3)
    friday = monday + timedelta(days=4)
    saturday = monday + timedelta(days=5)
    sunday = monday + timedelta(days=6)

    week_days = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    events_this_week = event_list.filter(
        start_date_time__gte=monday, start_date_time__lte=sunday + timedelta(days=1)
    )

    events_by_day = {}
    for day in week_days:
        events_by_day[day] = []

    for event in events_this_week:
        event_day = event.start_date_time.date()
        events_by_day[event_day].append(event)

    next_event = (
        Event.objects.filter(start_date_time__gte=timezone.now())
        .order_by("start_date_time")
        .first()
    )
    if next_event:
        time_difference = next_event.start_date_time - timezone.now()
        hours_until_next_event = time_difference.seconds // 3600
        minutes_until_next_event = (time_difference.seconds // 60) % 60
    else:
        hours_until_next_event = None
        minutes_until_next_event = None

    flag = True
    if request.user.is_authenticated:
        calendar_exist = Calendar.objects.filter(user=request.user).exists()
        if calendar_exist:
            flag = True

    context_dict = {
        "date": today_date,
        "flag": flag,
        "user": request.user,
        "calendars": calendar_list,
        "events_by_day": events_by_day,
        "week_days": week_days,
        "events_this_week": events_this_week,
        "next_event": next_event,
        "hours_until_next_event": hours_until_next_event,
        "minutes_until_next_event": minutes_until_next_event,
    }
    return render(request, f"{APP_TEMPLATE_DIR}index.html", context=context_dict)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user.user)
            return redirect("app:index")
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        user_form = UserRegistrationForm()
    return render(request, f"{APP_TEMPLATE_DIR}register.html", {"form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_profile = None
            try:
                user_profile = UserProfile.objects.get(user__username=username)
            except UserProfile.DoesNotExist:
                messages.error(request, "Username does not exist.")

            if user_profile is not None:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse("app:index"))
                else:
                    messages.error(request, "Incorrect password. Please try again.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LoginForm()
    return render(request, f"{APP_TEMPLATE_DIR}login.html", {"form": form})


@login_required
def profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile
        )

        if profile_form.is_valid():
            profile_form.save()
            return redirect("app:profile")
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(
        request,
        f"{APP_TEMPLATE_DIR}profile.html",
        {"profile_form": profile_form},
    )


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("app:index")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    else:
        form = PasswordChangeForm(request.user)
    return render(
        request, f"{APP_TEMPLATE_DIR}password_change_form.html", {"form": form}
    )


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse("app:index"))


@login_required
def calendars(request):
    return render(request, f"{APP_TEMPLATE_DIR}calendars.html")


@login_required
def events(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app:events")
    else:
        form = EventForm()

    search_q = request.GET.get("search", "")
    if search_q:
        events = Event.objects.filter(title__icontains=search_q)
    else:
        events = Event.objects.all()

    return render(
        request,
        f"{APP_TEMPLATE_DIR}events.html",
        {
            "form": form,
            "events": events,
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        },
    )


@login_required
def notifications(request):
    # it will now delete all events when the event has ended
    current_datetime = timezone.now()
    event_list = Event.objects.filter(end_date_time__gte=current_datetime).order_by(
        "start_date_time"
    )
    event_details = None
    event_id = request.GET.get("event_id")
    search_query = request.GET.get("search-bar", "")
    if search_query:
        event_list = (
            Event.objects.filter(end_date_time__gte=current_datetime)
            .filter(description__icontains=search_query)
            .order_by("start_date_time")
        )
    else:
        event_list = Event.objects.filter(end_date_time__gte=current_datetime).order_by(
            "start_date_time"
        )
    if event_id:
        event_details = get_object_or_404(Event, id=event_id)
    context_dict = {
        "events": event_list,
        "event_details": event_details,
        "search_query": search_query,
    }
    return render(request, f"{APP_TEMPLATE_DIR}notifications.html", context_dict)


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("app:index")

    return render(request, f"{APP_TEMPLATE_DIR}delete_account.html")
