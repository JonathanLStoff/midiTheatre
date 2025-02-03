from django.conf import settings
from miditheatre.extras.logger import LOGGER
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from miditheatre.models import action
from miditheatre.forms import ActionForm
from django.http import HttpRequest
import json


def action_manager(request:HttpRequest):
    actions = action.objects.all().order_by('order')
    return render(request, settings.TEMPLATES_FOLDER + '/actions/manager.html', {
        'actions': actions,
        'ordered_actions': actions.order_by('order')
    })

@require_http_methods(["POST"])
def create_action(request:HttpRequest):
    form = ActionForm(request.POST)
    if form.is_valid():
        LOGGER.info("Form is valid")
        action = form.save(commit=False)
        LOGGER.info("Form is saved")
        action.order = action.objects.count() + 1
        LOGGER.info("Order is set")
        action.save()
        LOGGER.info("Action is saved")
        return redirect('action_manager')
    return render(request, settings.TEMPLATES_FOLDER + '/actions/manager.html', {'form': form})

@require_http_methods(["POST"])
def reorder_actions(request:HttpRequest):
    order = json.loads(request.POST.get('order'))
    for index, action_id in enumerate(order):
        action.objects.filter(id=action_id).update(order=index)
    return redirect('action_manager')