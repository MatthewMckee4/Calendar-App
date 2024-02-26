from django.shortcuts import render, redirect
from app.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from app.forms import LoginForm

APP_TEMPLATE_DIR = "app/"


def index(request):
    return render(request, f"{APP_TEMPLATE_DIR}index.html")


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = UserRegistrationForm()
    return render(request, f"{APP_TEMPLATE_DIR}/register.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect(
                    "home"
                )  # Change 'home' to the name of your home page URL
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


@login_required
def profile(request):
    return render(request, f"{APP_TEMPLATE_DIR}profile.html")


@login_required
def logout_user(request):
    logout(request)
    return render(request, f"{APP_TEMPLATE_DIR}index.html")
