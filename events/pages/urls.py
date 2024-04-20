from django.contrib import admin
from . import views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('sjevents/signup', views.signup, name='signup'),
    path('sjevents/', views.test, name='real_homepage'),
    path('sjevents/profile', views.profile, name='profile'),
    re_path(r'^sjevents/events/$', views.all_events, name='all_events'),
    path('sjevents/event/<int:event_id>', views.event, name='event'),
    path('sjevents/club/<int:cid>', views.club, name='club'),

]
