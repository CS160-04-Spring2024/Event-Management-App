from django.contrib import admin
from . import views
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView


urlpatterns = [
    path('sjevents/signup', views.signup, name='signup'),
    path('sjevents/', views.test, name='real_homepage'),
    path('sjevents/profile', views.profile, name='profile'),
# <<<<<<< Jae2
#     path('sjevents/events', views.all_events, name='all_events'),
#     path('sjevents/event/id', views.event, name='event'),
#     path('sjevents/club/id', views.club, name='club'),
#     path('sjevents/admin/event/create', views.create_event, name='createEvent'),
#     path('sjevents/registered', views.user_registered_events, name='registeredEvents'), # user registered events
#     path('sjevents/search', views.search_results, name='searchResults'),
# =======
    re_path(r'^sjevents/events/$', views.all_events, name='all_events'),
    path('sjevents/event/<int:event_id>', views.event, name='event'),
    path('sjevents/club/<int:cid>', views.club, name='club'),

# >>>>>>> main
]
