from typing import List
from django import template
from app.models import Event, UserProfile
from django.conf import settings

register = template.Library()


@register.inclusion_tag("app/components/custom_input.html")
def custom_input(
    name: str,
    id: str,
    input_type: str,
    value: str = "",
    required=False,
    hidden=False,
    div_class: str = "",
    input_class: str = "",
    placeholder: str = "",
):
    return {
        "name": name,
        "id": id,
        "type": input_type,
        "value": value,
        "required": required,
        "hidden": hidden,
        "div_class": div_class,
        "input_class": input_class,
        "placeholder": placeholder,
    }


@register.inclusion_tag("app/components/custom_textarea.html")
def custom_textarea(name: str, id: str, value: str = "", required: bool = False):
    return {
        "name": name,
        "id": id,
        "value": value,
        "required": required,
    }


@register.inclusion_tag("app/components/custom_button.html")
def custom_button(text: str, button_type: str = "submit", extra_class: str = ""):
    return {"text": text, "type": button_type, "extra_class": extra_class}


@register.inclusion_tag("app/components/error_messages.html")
def error_messages(messages: List[str]):
    return {"messages": messages}


@register.inclusion_tag("app/components/event_list.html")
def user_profile_event_list(
    user_profile: UserProfile, card_type: str = "small_event_card"
):
    return event_list(user_profile.events.all(), card_type)


@register.inclusion_tag("app/components/event_list.html")
def event_list(events: List[Event], card_type: str = "small_event_card"):
    return {"events": events, "card_type": card_type}


@register.inclusion_tag("app/components/small_event_card.html")
def small_event_card(event: Event):
    return {"event": event, "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY}


@register.inclusion_tag("app/components/large_event_card.html")
def large_event_card(event: Event):
    return {"event": event}
