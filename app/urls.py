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
<<<<<<< HEAD
    path("profile-change/", views.change_profile_photo, name="profile_change")
=======
    path("notifications/", views.notifications, name="notifications"),
>>>>>>> 16bac45ab26e11094c11d253be0d4949e6118bca
]
