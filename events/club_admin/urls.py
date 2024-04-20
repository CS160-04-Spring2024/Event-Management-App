from django.contrib import admin
from . import views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('/event/create', views.create_event, name='createEvent'),

]
