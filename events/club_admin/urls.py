from django.contrib import admin
from . import views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('event/create', views.create_event, name='createEvent'),
    path('dashboard/admin', views.admin_dash, name='adminDash'),
    path('dashboard/admin/<club>', views.admin_dash_club, name='adminDashClub'),
    path('dashboard/admin/<club>/create-event',
         views.create_event, name='createEvent'),
    path('dashboard/admin/edit-club/<int:club_id>',
         views.edit_org, name='editClub'),
    path('dashboard/admin/<club>/edit-event/<int:event_id>/',
         views.edit_event, name='editEvent'),
    path('dashboard/admin/<club>/delete-event/<int:event_id>/',
         views.delete_event, name='deleteEvent'),

]
