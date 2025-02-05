import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from miditheatre.extras.keyboard_utils import keycode_to_name
from miditheatre.extras.logger import LOGGER
from miditheatre.forms import ActionForm, SettingsForm, PathForm
from miditheatre.models import action, settingUser, show, actionPath


def action_manager(request:HttpRequest):
    return render_main(request)

@require_http_methods(["POST"])
def create_action(request:HttpRequest):
    form = ActionForm(request.POST)
    if form.is_valid():
        LOGGER.info("Form is valid")
        form.save(commit=True)
        LOGGER.info("Form is saved")
        return redirect('action_manager')
    return render_main(request)

@require_http_methods(["POST"])
def create_path(request:HttpRequest):
    path_form = PathForm(request.POST)
    if path_form.is_valid():
        LOGGER.info("Form is valid")
        path_form.save(commit=True)
        LOGGER.info("Form is saved")
        return redirect('action_manager')
    return render_main(request)
    
def render_main(request:HttpRequest,  ac_form:ActionForm = ActionForm(), path_form:PathForm = PathForm()):
    if settingUser.objects.count() == 0:
        setting_for_user = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    else:
        setting_for_user = settingUser.objects.first()
    user_set = setting_for_user
    form_s = SettingsForm(initial={
        'theme': user_set.theme,
        'go_key': user_set.go_key,
        'stop_key': user_set.stop_key
    })
    actions:action = action.objects.all()
    shows = show.objects.all()
    if setting_for_user:
        show_current = setting_for_user.show_current
    else:
        show_current = None
        
    folders_path = create_folders(actionPath.objects.all())
    return render(
        request, 
        settings.TEMPLATES_FOLDER + '/actions/manager.html',
        {
            'actions': actions,
            'ordered_actions': [] if not show_current else show_current.actions,
            'form_a': ac_form, 
            'form_b': path_form,
            'form_s': form_s,
            'shows': shows,
            'action_dict': folders_path,
            }
        )
def create_folders(path_mod)->dict[str, Any]:
    '''Create a dictionary of folders and their children'''
    # Create two helper structures
    node_map = {}  # category -> children dict
    root = {}       # Resulting root nodes
    
    # First pass: create all nodes
    for item in path_mod:
        node_map[item.category] = {}
    
    # Second pass: build hierarchy
    for item in path_mod:
        category = item.category
        parent = item.parent
        
        if parent in node_map:
            # Add to parent's children
            node_map[parent][category] = node_map[category]
        else:
            # Add to root if parent doesn't exist or is None
            root[category] = node_map[category]
    
    return root
    
@require_http_methods(["POST"])
def reorder_actions(request:HttpRequest):
    order = json.loads(request.POST.get('order', "{}"))
    for index, action_id in enumerate(order):
        action.objects.filter(id=action_id).update(order=index)
    return redirect('action_manager')

@require_http_methods(["GET", "POST"])
def settings_view(request:HttpRequest):
    
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