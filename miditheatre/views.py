import json
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from asgiref.sync import sync_to_async

from miditheatre.extras.keyboard_utils import keycode_to_name
from miditheatre.extras.midi import MidiThread
from miditheatre.extras.logger import LOGGER
from miditheatre.forms import ActionForm, SettingsForm, PathForm, ShowForm
from miditheatre.models import action, settingUser, show, actionPath

MIDI = MidiThread()

def render_main(request:HttpRequest,  ac_form:ActionForm = ActionForm(), path_form:PathForm = PathForm()):
    if settingUser.objects.count() == 0:
        setting_for_user = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    elif settingUser.objects.count() > 1:
        for setting in settingUser.objects.all()[1:]:
            setting.delete()
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
    actions_list:dict[int, action] = {}
    if show_current:
        LOGGER.info("show_current.selected_action: %s", show_current.selected_action)
        LOGGER.info("show_current.actions: %s", show_current.actions)
        for act_id, actiony in enumerate(show_current.actions):
            actions_list[act_id] = action.objects.get(id=actiony)
        LOGGER.info("actions_list: %s", actions_list)
    return render(
            request,
            settings.TEMPLATES_FOLDER + '/actions/manager.html',
            {
                'actions': actions,
                'ordered_actions': [] if not show_current else show_current.actions,
                'go_key': user_set.go_key,
                'stop_key': user_set.stop_key,
                'form_a': ac_form, 
                'form_b': path_form,
                'form_s': form_s,
                'form_c': ShowForm(),
                'shows': shows,
                'selected_action': show_current.selected_action,
                'actions_list_dict': actions_list,
                'action_dict': folders_path,
                'template_f': settings.TEMPLATES_FOLDER + '/actions/folder_template.html',
            }
        )
@require_http_methods(["POST"])
async def select_change(request: HttpRequest) -> HttpResponse:
    """
    Handle POST request to select a change action.
    """

    index = request.POST.get('action_index')

    # Use sync_to_async to call the synchronous database operations
    @sync_to_async
    def get_setting_user():
        if settingUser.objects.count() == 0:
            setting_for_user = settingUser.objects.create(
                theme='dark',
                go_key=60,
                stop_key=61
            )
        else:
            setting_for_user = settingUser.objects.first()
        return setting_for_user
    @sync_to_async
    def get_show_user(setting_for_user):
        
        return setting_for_user.show_current
    setting_for_user = await get_setting_user()  # Await the result
    show_current:show = await get_show_user(setting_for_user)
    LOGGER.info("Show current: %s", show_current)
    if not show_current:
        return render(
            request,
            settings.TEMPLATES_FOLDER + '/actions/show_add.html',
            {
                "form_c": ShowForm(),
                "template_m": settings.TEMPLATES_FOLDER + '/actions/manager.html',
            }
        )

    show_current.selected_action = index
    
    @sync_to_async
    def save_show_user(show_current):
        show_current.save()

    await save_show_user(show_current)

    LOGGER.info(
        "Selected action: %s",
        show_current.selected_action
    )

    return HttpResponse(
        content=json.dumps(
            {
                "selected_action":
                show_current.selected_action
            }
        )
    )

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
@require_http_methods(["POST"])
async def go_view(request:HttpRequest):
    # Replace with actual go() function call
    if settingUser.objects.count() == 0:
        setting_for_user = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    else:
        setting_for_user = settingUser.objects.first()
    if not setting_for_user.show_current:
        return render(request,
        settings.TEMPLATES_FOLDER + '/actions/show_add.html',
        {
            'form_c': ShowForm(),
            'template_m': settings.TEMPLATES_FOLDER + '/actions/manager.html',
        }
        )
    
    action_id = setting_for_user.show_current.actions[setting_for_user.show_current.selected_action]
    action_obj:action = action.objects.get(id=action_id)
    LOGGER.info("Action: %s", action_obj)
    MIDI.go = True
    await MIDI.send_midi_message(action_obj.channel, action_obj.key, action_obj.value)
    if setting_for_user.show_current.selected_action == len(setting_for_user.show_current.actions) - 1:
        setting_for_user.show_current.selected_action = 0
    else:
        setting_for_user.show_current.selected_action += 1
    return render_main(request)

@require_http_methods(["POST"])
def stop_view(request:HttpRequest):
    # Replace with actual stop() function call
    MIDI.go = False
    return render_main(request)

@require_http_methods(["POST"])
def select_action_view(request:HttpRequest):
    # Replace with actual stop() function call
    if settingUser.objects.count() == 0:
        setting_for_user = settingUser.objects.create(
            theme='dark',
            go_key=60,
            stop_key=61
        )
    
    else:
        setting_for_user = settingUser.objects.first()
    if not setting_for_user.show_current:
        return render(request,
        settings.TEMPLATES_FOLDER + '/actions/show_add.html',
        {
            'form_c': ShowForm(),
            'template_m': settings.TEMPLATES_FOLDER + '/actions/manager.html',
        }
        )
    else:
        current_show:show = setting_for_user.show_current
    set_index = request.POST.get('action_index')
    current_show.selected_action = set_index
    current_show.save()
    return True


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
            'form_c': ShowForm(),
            'template_m': settings.TEMPLATES_FOLDER + '/actions/manager.html',
        }
        )
    else:
        current_show:show = setting_for_user.show_current 
    if isinstance(setting_for_user.show_current.actions, list):
        current_show.actions.append(request.POST.get('id'))
    else:
        current_show.actions = [request.POST.get('id')]
    current_show.save()
    return redirect('action_manager')


def create_folders(path_mod, action)->dict[str, Any]:
    '''Create a dictionary of folders and their children'''
    # Create two helper structures
    node_map = {}
    root = {}
    pk_map = {}
    for item_a in action:
        if item_a.path == "" or item_a.path is None:
            root[item_a.name] = f"MIDI (C:{item_a.channel} K:{item_a.key} V:{item_a.value})|{item_a.id}"
    # First pass: create all nodes
    for item in path_mod:
        node_map[item.category] = {}
        for item_a in action:
            if item_a.path:
                if item_a.path.pk == item.pk:
                    node_map[item.category][item_a.name] = f"MIDI (C:{item_a.channel} K:{item_a.key} V:{item_a.value})|{item_a.id}"
    
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

@require_http_methods(["POST"])
def settings_update(request:HttpRequest):
    setting_for_user = settingUser.objects.first()
    form = SettingsForm(request.POST, instance=setting_for_user)
    if form.is_valid():
        form.save(commit=True)
        return redirect('action_manager')
    return render_main(request)
