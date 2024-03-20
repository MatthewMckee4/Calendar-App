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
    path("create-event/", views.create_event, name="create_event"),
    path("notifications/", views.notifications, name="notifications"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path("events/", views.events, name="events"),
    path("event/<int:event_id>/", views.event, name="event"),
]
