from django.contrib import admin
from . import views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('event/create', views.create_event, name='createEvent'),
    path('dashboard/admin', views.admin_dash, name='adminDash'),
    path('dashboard/admin/<club>', views.admin_dash_club, name='adminDashClub'),
]
