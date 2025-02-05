import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from miditheatre.extras.keyboard_utils import keycode_to_name
from miditheatre.extras.logger import LOGGER
from miditheatre.forms import ActionForm, SettingsForm, PathForm, ShowForm
from miditheatre.models import action, settingUser, show, actionPath


def action_manager(request:HttpRequest):
    return render_main(request)

@require_http_methods(["POST"])
def create_action(request:HttpRequest):
    form = ActionForm(request.POST)
    if form.is_valid():
        LOGGER.info("Form is valid")
        model_saved = form.save(commit=True)
        LOGGER.info("Path: %s", model_saved.path)
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

@require_http_methods(["POST"])
def create_show(request:HttpRequest):
    show_form = ShowForm(request.POST)
    if show_form.is_valid():
        LOGGER.info("Form is valid")
        show_form.save(commit=True)
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
    form_s = SettingsForm(instance=user_set)
    actions:action = action.objects.all()
    shows = show.objects.all()
    if setting_for_user:
        show_current = setting_for_user.show_current
    else:
        show_current = None
        
    folders_path = create_folders(actionPath.objects.all(), action.objects.all())
    return render(
        request, 
        settings.TEMPLATES_FOLDER + '/actions/manager.html',
        {
            'actions': actions,
            'ordered_actions': [] if not show_current else show_current.actions,
            'form_a': ac_form, 
            'form_b': path_form,
            'form_s': form_s,
            'form_c': ShowForm(),
            'shows': shows,
            'action_dict': folders_path,
            'template_f': settings.TEMPLATES_FOLDER + '/actions/folder_template.html',
            }
        )
@require_http_methods(["POST"])
def additemshow(request:HttpRequest):
    if settingUser.objects.count() == 0:
        setting_for_user = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    else:
        setting_for_user = settingUser.objects.first()
    LOGGER.info("Setting SHOW: %s", setting_for_user.show_current)
    if not setting_for_user.show_current:
        return render(request,
        settings.TEMPLATES_FOLDER + '/actions/show_add.html',
        {
            'form_c': ShowForm()
        }
        )
    else:
        current_show:show = setting_for_user.show_current 
    if isinstance(setting_for_user.show_current.actions, list):
        current_show.actions.append(request.POST.get('id'))
    else:
        current_show.actions = [request.POST.get('id')]
    current_show.save()
    
def create_folders(path_mod, action)->dict[str, Any]:
    '''Create a dictionary of folders and their children'''
    # Create two helper structures
    node_map = {}
    root = {}
    pk_map = {}
    
    # First pass: create all nodes
    for item in path_mod:
        node_map[item.category] = {}
        for item_a in action:
            if item_a.path:
                if item_a.path.pk == item.pk:
                    node_map[item.category][item_a.name] = f"C:{item_a.channel} K:{item_a.key} V:{item_a.value}"
    
    # Second pass: build hierarchy
    for item in path_mod:
        category = item.category
        parent = str(item.parent).replace("/", "")
        if parent in node_map:
            # Add to parent's children
            node_map[parent][category] = node_map[category]
        else:
            # Add to root if parent doesn't exist or is None
            root[category] = node_map[category]
    LOGGER.info("Root: %s", root)
    return root
    
@require_http_methods(["POST"])
def reorder_actions(request:HttpRequest):
    order = json.loads(request.POST.get('order', "{}"))
    for index, action_id in enumerate(order):
        action.objects.filter(id=action_id).update(order=index)
    return redirect('action_manager')

