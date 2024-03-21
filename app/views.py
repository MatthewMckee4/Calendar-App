from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from app.forms import AddToCalendarForm, CalendarForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from app.forms import UserRegistrationForm, LoginForm, UserProfileForm, EventForm
from app.models import UserProfile, Calendar, Event
from app.utilities import get_events_json
from .models import Event
from datetime import date, timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone

APP_TEMPLATE_DIR = "app/"


def index(request):
    if not request.user.is_authenticated:
        return render(request, f"{APP_TEMPLATE_DIR}index.html")

    user_profile: UserProfile = request.user.userprofile
    calendar_list = Calendar.objects.filter(user=user_profile)
    event_list = user_profile.events.order_by("start_date_time")

    today_date = date.today()
    monday = today_date - timedelta(days=today_date.weekday())
    week_days = [monday + timedelta(days=i) for i in range(7)]

    events_this_week = event_list.filter(
        start_date_time__gte=monday, start_date_time__lte=monday + timedelta(days=6)
    )

    events_by_day = {day: [] for day in week_days}

    for event in events_this_week:
        event_day = event.start_date_time.date()
        events_by_day[event_day].append(event)

    week_day_events = {
        day.strftime("%A"): Event.objects.filter(start_date_time__date=day)
        for day in week_days
    }

    context = {
        "date": today_date,
        "week_day_events": week_day_events,
        "calendars": calendar_list,
        "events_by_day": events_by_day,
        "week_days": week_days,
        "events_this_week": events_this_week,
    }

    return render(request, f"{APP_TEMPLATE_DIR}index.html", context=context)


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
    calendars = Calendar.objects.filter(user=request.user.userprofile)
    return render(
        request, f"{APP_TEMPLATE_DIR}calendars.html", {"calendars": calendars}
    )


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user.userprofile
            event.save()
            form.save_m2m()
            return redirect("app:index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
                    messages.error(request, f"{field}: {error}")
    else:
        form = EventForm()

    return render(
        request,
        f"{APP_TEMPLATE_DIR}create_event.html",
        {
            "form": form,
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        },
    )


@login_required
def notifications(request):
    # it will now delete all events when the event has ended
    current_datetime = timezone.now()
    event_list = (
        (
            request.user.userprofile.events.all()
            | request.user.userprofile.attended_events.all()
        )
        .distinct()
        .order_by("start_date_time")
    )
    event = None
    attendees = []
    event_id = request.GET.get("event_id")
    search_query = request.GET.get("search-bar", "")
    if search_query:
        event_list = event_list.filter(name=search_query).order_by("start_date_time")
    else:
        event_list = event_list.filter(end_date_time__gte=current_datetime).order_by(
            "start_date_time"
        )
    if event_id:
        event = get_object_or_404(Event, id=event_id)
        attendees = event.attendees.all()
    context_dict = {
        "events": event_list,
        "event": event,
        "attendees": attendees,
        "search_query": search_query,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, f"{APP_TEMPLATE_DIR}notifications.html", context_dict)


@login_required
def delete_account(request):
    if request.method == "POST":
        request.user.delete()
        logout(request)
        return redirect("app:index")

    return render(request, f"{APP_TEMPLATE_DIR}delete_account.html")


@login_required
def events(request):
    event_list = Event.objects.filter(owner=request.user.userprofile)
    return render(request, f"{APP_TEMPLATE_DIR}events.html", {"events": event_list})


@login_required
def event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees.all()
    if request.method == "POST":
        form = AddToCalendarForm(
            request.POST, user=request.user.userprofile, event=event
        )
        if form.is_valid():
            form.save()
            return redirect("app:event", event_id=event_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
                    messages.error(request, f"{field}: {error}")
    else:
        form = AddToCalendarForm(user=request.user.userprofile, event=event)
    return render(
        request,
        f"{APP_TEMPLATE_DIR}event.html",
        {
            "event": event,
            "form": form,
            "attendees": attendees,
            "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        },
    )


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect("app:index")


@login_required
def calendar_delete(request, calendar_id):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    calendar.delete()
    return redirect("app:index")


@login_required
def create_calendar(request):
    if request.method == "POST":
        form = CalendarForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.user = request.user.userprofile
            calendar.save()
            form.save_m2m()
            return redirect("app:index")
    else:
        form = CalendarForm(initial={"events": []})
    return render(request, f"{APP_TEMPLATE_DIR}create_calendar.html", {"form": form})


@login_required
def calendar(request, calendar_id):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    events = get_events_json(calendar.events.all())
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user.userprofile
            event.save()
            return redirect("app:index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = EventForm()
    return render(
        request,
        f"{APP_TEMPLATE_DIR}calendar.html",
        {"calendar": calendar, "events": events, "form": form},
    )
