from typing import List
from django import template

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
