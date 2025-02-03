
from django.http import HttpRequest

def theme_context(request:HttpRequest):
    return {
        'current_theme': request.session.get('theme', 'dark'),
        'go_key': request.session.get('go_key', 60),
        'stop_key': request.session.get('stop_key', 61)
    }