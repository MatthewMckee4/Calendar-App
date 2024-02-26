from django.contrib import admin
from app.models import UserProfile, Calendar, Reminder, Tag, Event, Invitation

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass


class CalendarAdmin(admin.ModelAdmin):
    pass


class ReminderAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class InvitationAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Invitation, InvitationAdmin)
