from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def edit_event(request, event_id):
    if request.method == 'GET':
        event = Event.objects.get(pk=event_id)

        return render(request, 'editEvent.html', {'event': event})

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        fees = request.POST.get('fees')
        club = request.POST.get('club')

        Event.objects.filter(pk=event_id).update(event_name=name, description=description,
                                                 location=location, start_time=start, end_time=end, fees=fees, organization=club)

    return HttpResponse('Some Error has occured')


@api_view(['GET', 'POST'])
def create_event(request):
    if request.method == 'GET':

        return render(request, 'createEvent.html', {'form': EventForm()})
   # form = EventForm(request.POST or None)
    if request.method == 'POST':
        form = EventForm(request.POST)
        print(form.errors)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.organization = Organization.objects.get(pk=1)
            inst.save()

            return HttpResponseRedirect(reverse('real_homepage'))
        else:
            return render(request, 'createEvent.html', {'form': form})
    return render(request, 'createEvent.html', {'form': EventForm()})


def create_org(request):
    if request.method == 'GET':

        return render(request, 'create_club.html', {})

    # if request.method == 'POST':


def edit_org(request, id):
    if request.method == 'GET':
        org = Organization.objects.get(pk=id)

        return render(request, 'edit_club.html', {'club': org})

    if request.method == 'POST':
        club_name = request.POST.get('name')
        description = request.POST.get('description')
        location_id = request.POST.get('location_id')
        banner = request.POST.get('banner', None)
        club_logo = request.POST.get('logo', None)
        club_email = request.POST.get('email', None)
        website = request.POST.get('website', None)

        Organization.objects.filter(pk=id).update(name=club_name, description=description, location=location_id,
                                                  banner=banner, club_logo=club_logo, club_email=club_email, website=website)
