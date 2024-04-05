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


def all_events(request):
    return render(request, 'all_events.html', {})
