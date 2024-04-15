from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import EventForm
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def test(request):
    return render(request, 'homebase.html', {})


@api_view(['GET', 'POST'])
def profile(request):

    if request.method == 'GET':

        return render(request, 'profile.html', {})

    if request.method == 'POST':
        # is_admin = request.POST.get('is_admin')
        # if is_admin == 'True':
        #     club = request.POST.get('selected_club_id')
        email = request.user.email
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('dept')
        major = request.POST.get('major')
        funds = request.POST.get('funds')
        role = request.POST.get('role')

        # if test is None:
        #     User.objects.create(user_email=email, first_name=first_name, last_name=last_name,
        #                         role=role, department=department, funds=funds, major=major)

        # else:
        curr_user = User.objects.get(pk=email)
        old_funds = curr_user.funds
        new_funds = old_funds + funds
        User.objects.filter(pk=email).update(first_name=first_name, last_name=last_name,
                                             role=role, department=department, funds=new_funds, major=major)

    return render(request, 'profile.html', {})


@api_view(['GET', 'POST'])
def signup(request):

    email = request.user.email
    if User.objects.filter(pk=email).exists():
        return HttpResponseRedirect(reverse('real_homepage'))

    if request.method == 'GET':
        tags = Tag.objects.all()
        departments = Department.objects.all()
        majors = Major.objects.all()
        clubs = Organization.objects.all()

        return render(request, 'signup.html', {'tags': tags, 'departments': departments, 'majors': majors, 'clubs': clubs})

    if request.method == 'POST':
        email = request.POST.get('email', None)
        is_admin = request.POST.get('is_admin', None)
        if is_admin == 'True':
            club = request.POST.get('selected_club_id', None)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('dept')
        major = request.POST.get('major')
        funds = request.POST.get('funds')
        role = request.POST.get('role', None)

        print(dict(request.POST.items()))
        if email is not None and is_admin != None and role != None:
            # User.objects.create(user_email=email, first_name=first_name, last_name=last_name,
            #                     role=role, department=department, funds=funds, major=major)
            tags = request.POST.get('selectedTags', [])
            return HttpResponseRedirect(reverse('real_homepage'))
        else:
            return HttpResponse('Some Error has occured')
        # if is_admin == 'True':
        #     club = request.POST.get('selected_club_id', None)
        #     Admin.objects.create(user_email=email, organization=club)

    return render(request, 'signup.html', {})


@api_view(['GET'])
def event(request, event_id):
    if request.method == 'GET':
        event = Event.objects.get(pk=event_id)
        return render(request, 'event.html', {'event_id': event})
    return render(request, 'event.html', {})


def club(request, cid):
    if request.method == 'GET':
        # club = Organization.objects.get(pk=cid)
        club = None
        if club is None:
            return render(request, 'club.html')

        all_club_events = Event.objects.get(club_id=cid)
        return render(request, 'club.html', {'club': club, 'events': all_club_events})
    return HttpResponse('Some Error has occured')


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


@api_view(['POST'])
def create_event(request):
   # form = EventForm(request.POST or None)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')
        fees = request.POST.get('fees')
        club = request.POST.get('club')

    Event.objects.create(event_name=name, description=description, location=location,
                         start_time=start, end_time=end, fees=fees, organization=club)
    return render(request, 'createEvent.html', {'form': EventForm()})


@api_view(['GET'])
def user_events(request):
    if request.method == 'GET':
        email = request.user.email
        user_events = Registration.objects.get(user_email=email)

        my_events = []
        for event in user_events:
            my_events.append(Event.objects.get(pk=event.id))

        return render(request, 'user_events.html', {'my_events': my_events})


def delete_user_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse('user_events'))


@api_view(['GET'])
def all_events(request):
    if request.method == 'GET':
        all_events = Event.objects.all()
        return render(request, 'all_events.html', {'events': all_events})
    return render(request, 'all_events.html', {})


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
