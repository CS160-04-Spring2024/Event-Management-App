from urllib.parse import urlencode
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import random
import json
import datetime
from django.db import connection
# Create your views here.


tags = Tag.objects.all()
majors = Major.objects.all()
departments = Department.objects.all()

# json serialize for datetime object


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def datetime_to_string(start_date, end_date):
    dotw = start_date.strftime('%a')
    dotw_end = end_date.strftime('%a')
    format = '%H:%M %p'
    totw = start_date.strftime(format)
    totw_end = end_date.strftime(format)

    if dotw != dotw_end:
        return dotw + " " + totw + " - " + dotw_end + " " + totw_end

    return dotw + " " + totw + " - " + totw_end


def test(request):
    # person = User.objects.filter(pk=request.user.email).values()
    return render(request, 'home.html', {'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})


def main_page(request):
    if request.method == 'GET':
        user_email = request.user.email

        # pull events based on matching tags
        user_tags = UserInterest.objects.values('tag').filter(user=user_email)

        events = set()
        for user_tag in user_tags:
            tag_events = EventTag.objects.filter(tag=user_tag.tag)

            # assuming this gives the event ids of for all associated tags
            for ev in tag_events:
                events.add(ev.event)  # add to set to avoid repetitions

        # get all events
        tag_events_arr = []
        for x in events:
            one_event = Event.objects.filter(pk=x.event_id)
            tag_events_arr.extend(one_event)

        '''
        # Pull events based on department
        user_dept = User.objects.values('department').get(user=user_email)

        if user_dept is not None:
            dept_events_arr = []
            dept_clubs = ClubDepartment.objects.filter(department = user_dept.department)

            #shuffling array of clubs
            random.shuffle(dept_clubs)
            
            if len(dept_clubs) > 2:
                dept_clubs = dept_clubs[:2]
            
            for club in dept_clubs:
                club_events = Event.objects.filter(organization = club.club_id)
                dept_events_arr.extend(club_events)
        
            # pull clubs that the user may be interested in checking out

            random.shuffle(dept_clubs)

            club_list = []

            if len(dept_clubs) > 2:
                    dept_clubs = dept_clubs[:3]
            

            for club in dept_clubs:
                clubs = Organization.objects.get(pk=club.id)

                club_list.extend(clubs)
        '''


@api_view(['GET', 'POST'])
def profile(request):

    email = request.user.email
    if request.method == 'GET':
        person = User.objects.get(pk=email)
        # user_tags = User.objects.values('tag').filter(user=email)
        # user_profile = UserInterest.objects.filter(user=email)
        profile_form = ProfileForm(instance=person, initial={
                                   'tags': person.tags.all()})

        return render(request, 'profile.html', {'person': User.objects.filter(pk=email).values(), 'form': profile_form})

    if request.method == 'POST':
        person = User.objects.get(pk=request.user.email)
        profile_form = ProfileForm(request.POST, instance=person)

        if profile_form.is_valid():
            # print('saving FORM....')
            # print(profile_form.cleaned_data)
            profile_form.save()
            # all_tags = person.tags.all()
            # for tag in profile_form.cleaned_data['tags']:
            #     if tag not in all_tags:
            #         person.tags.add(tag)

            return HttpResponseRedirect(reverse('real_homepage'))

    return render(request, 'profile.html', {'form': profile_form, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})


@api_view(['GET', 'POST'])
def signup(request):

    email = request.user.email
    if User.objects.filter(pk=email).exists():
        return HttpResponseRedirect(reverse('real_homepage'))

    if request.method == 'GET':
        user_form = ProfileForm()
        club_form = AdminForm()
        return render(request, 'signup.html', {'form': user_form, 'club_form': club_form})

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        admin_form = AdminForm(request.POST)

        if profile_form.is_valid() and admin_form.is_valid():
            org = admin_form.cleaned_data['organization']
            profile_form.save()

            Admin.objects.create(user=email, organization=org)

            return HttpResponseRedirect(reverse('real_homepage'))

    return HttpResponseRedirect(reverse('signup'))


@api_view(['GET', 'POST'])
def event(request, event_id):

    if request.method == 'GET':
        event = Event.objects.filter(pk=event_id).values()[0]
        # departments = Department.objects.all()
        # tags = Tag.objects.all()
        event['club_name'] = Organization.objects.filter(
            pk=event['organization_id']).values_list('name', flat=True)
        event['time'] = datetime_to_string(
            event['start_time'], event['end_time'])
        event['attendees'] = Registration.objects.filter(
            event=event['event_id']).count()

        new_event = Event.objects.get(pk=event['event_id'])
        event['tag_list'] = new_event.tags.all().values_list(flat=True)

        current_tags = event['tag_list']
        all_events = Event.objects.all().values()
        # print(event)

        similar_values = []
        for eve in all_events:
            new_event = Event.objects.get(pk=eve['event_id'])
            if len(list(set(current_tags) & set(new_event.tags.all().values_list(flat=True)))) > 0 and eve['id'] != event_id:
                similar_values.append(eve)

        club = Organization.objects.filter(
            pk=event['organization_id']).values()

        location = Location.objects.filter(pk=event['location_id']).values()
        registered = Registration.objects.filter(
            user_email=request.user.email, event=event_id).exists()
        # print(registered)
        '''
        , 'club': club[0], 'location': location, 'similar_events': similar_events, 'registered': registered, 'event_tags': tags, 'time': event_time
        '''

        return render(request, 'event.html', {'event': event, 'similar_values': similar_values[:3], 'club': club[0], 'location': location[0], 'registered': registered, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})

    if request.method == 'POST':
        if request.POST.get('register'):
            if Registration.objects.filter(
                    user_email=request.user.email, event=event_id).exists() == False:
                Registration.objects.create(
                    user_email=User.objects.get(pk=request.user.email), event=Event.objects.get(pk=event_id))
            else:
                Registration.objects.filter(
                    user_email=request.user.email, event=event_id).delete()

            return HttpResponseRedirect(reverse('event', args=[event_id]))

    print('Ending Up here?')
    return render(request, 'event.html', {})


def club(request, cid):
    if request.method == 'GET':
        club = Organization.objects.filter(pk=cid).values()

        if club.exists() == False:
            return HttpResponse('Some Error has occured')

        all_club_events = Event.objects.filter(organization=cid).values()

        for event in all_club_events:
            event['club_name'] = Organization.objects.values(
                'name').filter(id=event['organization_id'])[0]['name']
            event['time'] = datetime_to_string(
                event['start_time'], event['end_time'])
            event['attendance'] = Registration.objects.filter(
                event=event['event_id']).count()

        location = Location.objects.filter(
            location_id=club[0]['location_id']).values()

        return render(request, 'club.html', {'club': club[0], 'events': all_club_events, 'location': location[0], 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})

    return HttpResponse('Some Error has occured')


@api_view(['GET'])
def user_events(request):
    email = request.user.email

    if request.method == 'GET':
        all_registered = Registration.objects.filter(user_email=email).values()
        departments = Department.objects.all()
        tags = Tag.objects.all()
        user_tag = request.GET.get('tag')

        all_events = [Event.objects.filter(
            pk=reg['event_id']).values()[0] for reg in all_registered]

        if user_tag:
            new_events = []

            for event in all_events:
                new_event = Event.objects.get(pk=event['event_id'])
                if new_event.tags.exists() and user_tag in new_event.tags:
                    new_events.append(event)
            all_events = new_events

        all_events = extra_event_params(all_events)

    return render(request, 'registered.html', {'events': all_events, 'departments': departments, 'tags': tags, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})


def delete_user_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return HttpResponseRedirect(reverse('user_events'))


@api_view(['GET', 'POST'])
def all_clubs(request):
    all_clubs = Organization.objects.all()
    search_word = None
    if request.method == 'GET':
        search_word = request.GET.get('search')
        if search_word:
            results = Organization.objects.filter(Q(name__contains=search_word) | Q(
                description__contains=search_word)).values()

        for club in all_clubs.values():
            club['description'] = ' '.join(club['description'].split(' ')[:10])

    if request.method == 'POST':
        dept = request.POST.get('dept')

        if dept:
            all_clubs = all_clubs.filter(
                department_id=Department.objects.get(pk=dept)).values()

    if not search_word:
        results = None

    if search_word and len(results) == 0:
        results = -1

    departments = Department.objects.all().values()
    return render(request, 'all_clubs.html', {'search': results, 'clubs': all_clubs, 'departments': departments, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin']})


@api_view(['GET', 'POST'])
def all_events(request):

    if request.method == 'GET':
        search_word = request.GET.get('search')
        if search_word:
            results = Event.objects.filter(Q(event_name__contains=search_word) | Q(
                description__contains=search_word)).values()
        all_events = Event.objects.all().order_by('-start_time').values()

    if request.method == 'POST':
        sort = request.POST.get('sort', 1)
        dept = request.POST.get('dept', None)
        minPrice = request.POST.get('min_price', None)
        maxPrice = request.POST.get('max_price', None)
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        selected_tags = request.POST.get('selectedTags', None)

        sorter = '-start_time' if sort == 1 else 'start_time'
        # print('selected: ', selected_tags)
        all_events = Event.objects.all().order_by(sorter).values()

        if minPrice:
            all_events = all_events.filter(fees__gte=minPrice)
        if maxPrice:
            all_events = all_events.filter(fees__lte=maxPrice)

        if start_date:
            all_events = all_events.filter(start_time__gte=start_date)
        if end_date:
            all_events = all_events.filter(end_time__gte=end_date)

        if dept:
            new_all_events = []
            for event in all_events:
                dpt = Organization.objects.filter(
                    pk=event['organization_id']).values()[0]['department_id']
                if dpt == dept:
                    new_all_events.append(event)
            all_events = new_all_events
        if selected_tags:
            tags = selected_tags.split(',')
            # print(tags)

            all_events = Event.objects.filter(
                tags__in=tags).distinct().values()

    if search_word:
        results = extra_event_params(results)
    all_events = extra_event_params(all_events)

    if not search_word:
        results = None
    print(results)
    # return redirect(reverse('all_events') )
    departments = Department.objects.all()
    all_tags = Tag.objects.all()
    return render(request, 'all_events.html', {'events': all_events, 'departments': departments, 'tags': all_tags, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'], 'search': results})


# search page
@api_view(['GET', 'POST'])
def search_page(request):
    view = 'all_events'
    new_search = ''

    if request.method == 'POST':
        option = request.POST.get('option', '0')
        search_word = request.POST.get('search', None)

        if option == '0':
            view = 'all_events'
            new_search = '?search='+search_word

        if option == '1':
            view = 'all_clubs'
            new_search = '?search=' + search_word

        # have to pass into events page or club page with the new results as query parameters
    return HttpResponseRedirect(reverse(view) + new_search)


'''
Takes a list of events and adds 
extra params for detailed event card
'''


def extra_event_params(events):
    for event in events:
        event['club_name'] = Organization.objects.filter(
            pk=event['organization_id']).values_list('name', flat=True)[0]
        event['time'] = datetime_to_string(
            event['start_time'], event['end_time'])
        event['attendees'] = Registration.objects.filter(
            event=event['event_id']).count()
        new_event = Event.objects.get(pk=event['event_id'])
        event['tag_list'] = new_event.tags.all()

    return events
