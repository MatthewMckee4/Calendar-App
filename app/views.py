from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from app.forms import LoginForm
from app.forms import UserRegistrationForm, LoginForm, UserProfileForm
from datetime import date
from app.models import UserProfile
from app.models import Calendar

APP_TEMPLATE_DIR = "app/"


def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("app:index"))
    else:
        form = LoginForm()
    flag = False
    if request.user.is_authenticated:
        calendar_exist = Calendar.objects.filter(user=request.user).exists()
        if calendar_exist:
            flag = True
    context_dict = {'date': date.today(), 'form': form, 'flag': flag, 'user': request.user}
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
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("app:index"))
    else:
        form = LoginForm()
    return render(request, f"{APP_TEMPLATE_DIR}login.html", {"form": form})


@login_required
def profile(request):
    context_dict = {}

    full_name_list = request.user.get_full_name().split(" ")
    context_dict["fname"] = full_name_list[0]
    context_dict["lname"] = full_name_list[1]

    userProfile = UserProfile.objects.get(user = request.user)
    if userProfile:
        context_dict["DoB"] = userProfile.date_of_birth
        context_dict["profilePhoto"] = userProfile.profile_picture_url
    return render(request, f"{APP_TEMPLATE_DIR}profile.html", context=context_dict)


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse("app:index"))


@login_required
def calendars(request):
    return render(request, f"{APP_TEMPLATE_DIR}calendars.html")