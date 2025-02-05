from django import template

register = template.Library()

@register.filter
def split(value:str, arg:str)->list[str]:
    return value.split(arg)