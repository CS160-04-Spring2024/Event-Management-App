from datetime import date, timezone
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.


def admin_dash(request):
    # Fetch organization IDs where the current user is an admin
    admin_orgs_ids = Admin.objects.filter(
        user_id=request.user.email).values_list('organization_id', flat=True)
    # print(request.user.id)
    # print(admin_orgs_ids[0])
    # Use the fetched IDs to filter organizations
    user_clubs = Organization.objects.filter(id__in=admin_orgs_ids)
    clubs = list(user_clubs)
    # print(user_clubs)

    return render(request, 'admin_dash.html', {'clubs': clubs, 'admin_id': admin_orgs_ids[0]})


def admin_dash_club(request, club):
    organization = Organization.objects.get(name=club)
    
    # Fetch current events (events whose end_time is in the future)
    current_events = Event.objects.filter(organization=organization, end_time__gte=timezone.now()).values()

    # Fetch past events (events whose end_time is in the past)
    past_events = Event.objects.filter(organization=organization, end_time__lt=timezone.now()).values()

    # Create a dictionary to store registered users for each event
    # Fetch registered users for each current event
    for event in current_events:
       event["registered_user"] = Registration.objects.filter(event=event["event_id"]).values()

    # Fetch registered users for each past event
    for event in past_events:
        event["registered_user"]  = Registration.objects.filter(event=event["event_id"]).values_list('user_email', flat=True)


    return render(request, 'admin_dash_club.html', {'club': club, 'current_events': current_events, 'past_events': past_events})

def edit_event(request, club, event_id):
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            # Pass club as argument
            return HttpResponseRedirect(reverse('adminDashClub', args=[club]))
    else:
        form = EventEditForm(instance=event)

    return render(request, 'event_admin_edit.html', {'form': form, 'event': event, 'club': club})


@api_view(['GET', 'POST'])
def create_event(request):
    if request.method == 'GET':
        return render(request, 'createEvent.html', {'form': EventForm()})
   # form = EventForm(request.POST or None)
    if request.method == 'POST':
        form = EventForm(request.POST)
        # print(request.POST.items)
        if form.is_valid():
            # print('IN HERE!!!!!')
            inst = form.save(commit=False)
            org_id = Admin.objects.filter(user=request.user.email).values()
            if len(org_id) > 0:
                inst.organization = Organization.objects.get(
                    pk=org_id[0]['organization_id'])
            else:
                inst.organization = Organization.objects.get(
                    pk=2)
            inst.save()
            form.save_m2m()

            return HttpResponseRedirect(reverse('real_homepage'))
        else:
            return render(request, 'createEvent.html', {'form': form})
    return render(request, 'createEvent.html', {'form': EventForm()})


@api_view(['POST'])
def delete_event(request, club, event_id):
    # Retrieve the event object to be deleted
    if request.method == 'POST':

        event = Event.objects.get(pk=event_id)

        # Perform the deletion operation
        event.delete()

        # Redirect to a success URL or render a template
        # Redirect to admin dashboard or wherever you want
        return HttpResponseRedirect(reverse('adminDashClub', args=[club]))


def edit_org(request, club_id):
    org = Organization.objects.get(pk=club_id)

    if request.method == 'POST':
        form = ClubForm(request.POST, instance=org)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('adminDash'))

    else:
        form = ClubForm(instance=org)

    return render(request, 'club_edit.html', {'form': form, 'organization': org, 'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})
