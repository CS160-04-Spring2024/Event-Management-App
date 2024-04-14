from django.contrib import admin
from . import views
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path('', views.home, name='homepage'),

]
