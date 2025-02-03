import json

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from miditheatre.extras.keyboard_utils import keycode_to_name
from miditheatre.extras.logger import LOGGER
from miditheatre.forms import ActionForm, SettingsForm
from miditheatre.models import action, settingUser


def action_manager(request:HttpRequest):
    actions = action.objects.all().order_by('order')
    form = ActionForm()
    return render(request, settings.TEMPLATES_FOLDER + '/actions/manager.html', {
        'actions': actions,
        'ordered_actions': actions.order_by('order'),
        'form_a': form
    })

@require_http_methods(["POST"])
def create_action(request:HttpRequest):
    form = ActionForm(request.POST)
    if form.is_valid():
        LOGGER.info("Form is valid")
        action = form.save(commit=False)
        LOGGER.info("Form is saved")
        action.order = action.__class__.objects.count() + 1
        LOGGER.info("Order is set")
        action.save()
        LOGGER.info("Action is saved")
        return redirect('action_manager')
    return render(request, settings.TEMPLATES_FOLDER + '/actions/manager.html', {'form_a': form})

@require_http_methods(["POST"])
def reorder_actions(request:HttpRequest):
    order = json.loads(request.POST.get('order', "{}"))
    for index, action_id in enumerate(order):
        action.objects.filter(id=action_id).update(order=index)
    return redirect('action_manager')

@require_http_methods(["GET", "POST"])
def settings_view(request:HttpRequest):
    if settingUser.objects.count() == 0:
        user_set = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    else:
        user_set = settingUser.objects.first()
    form = None
    if user_set:
        if request.method == 'POST':
            form = SettingsForm(request.POST)
            if form.is_valid():
                # Save settings to session
                request.session['theme'] = form.cleaned_data['theme']
                request.session['go_key'] = form.cleaned_data['go_key']
                request.session['stop_key'] = form.cleaned_data['stop_key']
                user_set.theme = form.cleaned_data['theme']
                user_set.go_key = form.cleaned_data['go_key']
                user_set.stop_key = form.cleaned_data['stop_key']
                user_set.save()
                LOGGER.info("Settings saved")
                return redirect('settings')
        else:
            LOGGER.info("No POST request")
            LOGGER.info("Creating form with: %s, %s, %s", user_set.theme, user_set.go_key, user_set.stop_key)
            form = SettingsForm(initial={
                'theme': user_set.theme,
                'go_key': user_set.go_key,
                'stop_key': user_set.stop_key
            })
    else:
        LOGGER.error("No settings found")
    if form and user_set:
        return render(request, settings.TEMPLATES_FOLDER + '/actions/settings.html', {'form': form, 'gokey_label': keycode_to_name(user_set.go_key), 'stopkey_label': keycode_to_name(user_set.stop_key)})