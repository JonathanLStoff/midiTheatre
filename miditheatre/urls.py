"""
URL configuration for miditheatre project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from miditheatre import views
from typing import Any

urlpatterns:list[Any] = [
    path('admin/', admin.site.urls),
    path('', views.action_manager, name='action_manager'),
    path('create/', views.create_action, name='create_action'),
    path('reorder/', views.reorder_actions, name='reorder_actions'),
    path('settings/', views.settings_view, name='settings'),
]