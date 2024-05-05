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
    admin_orgs_ids = Admin.objects.filter(user_id=request.user.email).values_list('organization_id', flat=True)
    print(request.user.id)
    # Use the fetched IDs to filter organizations
    user_clubs = Organization.objects.filter(id__in=admin_orgs_ids)
    clubs = list(user_clubs)
    print(user_clubs)

    return render(request, 'admin_dash.html', {'clubs': clubs})

def admin_dash_club(request, club):

    # Assuming 'club' parameter is the name of the club. Adjust the filter accordingly if it's an ID or another field.
    organization = Organization.objects.get(name=club)
    # Fetch events for the organization
    events = Event.objects.filter(organization=organization)

    return render(request, 'admin_dash_club.html', {'club': club, 'events': events})


def edit_event(request, club, event_id):
    event = Event.objects.get(pk=event_id)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminDashClub', args=[club]))  # Pass club as argument
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
            print('IN HERE!!!!!')
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

@api_view([ 'POST'])
def delete_event(request, club, event_id):
    # Retrieve the event object to be deleted
        if request.method == 'POST':

            event = Event.objects.get(pk=event_id)

            # Perform the deletion operation
            event.delete()

            # Redirect to a success URL or render a template
            return HttpResponseRedirect(reverse('adminDashClub', args=[club]))  # Redirect to admin dashboard or wherever you want
# Pass club as argument

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
        

