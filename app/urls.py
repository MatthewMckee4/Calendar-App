from django.urls import path
from app import views


app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout_user, name="logout"),
    path("calendars/", views.calendars, name="calendars"),
    path("password-change/", views.change_password, name="password_change"),
    path("events/", views.events, name="events"),
]
