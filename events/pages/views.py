from django.shortcuts import render
from .forms import EventForm
# Create your views here.


def test(request):
    return render(request, 'homebase.html', {})


def profile(request):
    return render(request, 'profile.html', {})


def event(request):
    return render(request, 'event.html', {})


def club(request):
    return render(request, 'club.html', {})


def create_event(request):
   # form = EventForm(request.POST or None)
    return render(request, 'createEvent.html', {'form': EventForm()})

def user_registered_events(request): # render user registered event page
    return render(request, 'user_registered_events.html', {})

def search_results(request): # render user's query {events, clubs, departments}
    return render(request, 'search_results.html', {})

def all_events(request):
    return render(request, 'all_events.html', {})
