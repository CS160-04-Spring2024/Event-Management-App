from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from rest_framework.decorators import api_view
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.db.models.functions import Random
from django.urls import reverse
from django.db.models import Q
import random
import json
import datetime
import pytz
from django.db import connection
# Create your views here.


tags = Tag.objects.all()
majors = Major.objects.all()
departments = Department.objects.all()

# json serialize for datetime object


def Errorhandler404(request, exception):
    content = loader.render_to_string(
        '404.html', {}, request)
    return HttpResponseNotFound(content)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def datetime_to_string(start_date, end_date):
    utc_start = start_date.replace(tzinfo=pytz.UTC)
    localtz_start = utc_start.astimezone(timezone.get_current_timezone())
    utc_end = end_date.replace(tzinfo=pytz.UTC)
    localtz_end = utc_end.astimezone(timezone.get_current_timezone())

    dotw = localtz_start.strftime('%a')
    dotw_end = localtz_end.strftime('%a')
    format = '%H:%M %p'
    totw = localtz_start.strftime(format)
    totw_end = localtz_end.strftime(format)

    if dotw != dotw_end:
        return dotw + " " + totw + " - " + dotw_end + " " + totw_end

    return dotw + " " + totw + " - " + totw_end


def get_similar_events(past_events):

    similar_values = []
    event_tags = set()
    event_ids = []
    for eve in past_events:
        current_tags = eve.tags.all().values_list(flat=True)
        event_ids.append(eve.event_id)
        event_tags.update(current_tags)

    all_events = Event.objects.filter(end_time__gt=datetime.date.today())

    for eve in all_events:
        new_event = Event.objects.filter(pk=eve.event_id)
        eve_tags = eve.tags.all().values_list(flat=True)
        new_event = new_event.values()[0]

        if len(eve_tags) > 0:
            if len(set(list(current_tags) + (list(eve_tags)))) < len(eve_tags) + len(current_tags) and eve.event_id not in event_ids:
                similar_values.append(new_event)

    print(similar_values)
    similar_values = extra_event_params(similar_values)


def test(request):
    # person = User.objects.filter(pk=request.user.email).values()
    return render(request, 'home.html', {'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'], 'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})


@api_view(['GET'])
def main_page(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_email = request.user.email

            clubs = Organization.objects.all().order_by(Random()).values()
            user_info = User.objects.filter(pk=user_email).values()[0]

            club_of_week = clubs[0]

            user_tags = User.objects.get(pk=user_email).tags.all()
            all_events = Event.objects.filter(
                end_time__gt=datetime.date.today()).values()

            # events by user tag
            # personalized_tag_events = Event.objects.filter(
            #     tags__in=user_tags).values()

            # attempting to compare all tag events and sort them by
            # order of decreasing similarity to user tags
            personalized_tag_events = []
            tags_dict = {}
            for event in all_events:
                event_tags = list(Event.objects.get(
                    pk=event['event_id']).tags.all())

                intersect_size = len(set(event_tags) & set(user_tags))

                if intersect_size not in tags_dict:
                    tags_dict[intersect_size] = [event]

                else:
                    tags_dict[intersect_size].append(event)

            dict_keys = sorted(list(tags_dict.keys()), reverse=True)
            # print(dict_keys)

            for k in dict_keys:
                personalized_tag_events.extend(tags_dict[k])

            personalized_tag_events = personalized_tag_events[:10]

            # filtering by department
            if user_info['department_id']:
                personalized_departments = []
                for event in all_events:
                    org = Organization.objects.filter(
                        id=event['organization_id']).values()[0]
                    if user_info['department_id'] == org['department_id']:
                        personalized_departments.append(event)

            personalized_tag_events = extra_event_params(
                personalized_tag_events)

            # registered events
            all_registered = Registration.objects.filter(
                user_email=user_email).values()

            all_registered_events = [Event.objects.filter(
                pk=reg['event_id'], end_time__gt=datetime.date.today()).values()[0] for reg in all_registered]

            # recommended based on past events
            past_events = Event.objects.filter(
                end_time__lt=datetime.date.today())
            # print(past_events)
            if len(past_events) > 0:
                similar_current_events = get_similar_events(
                    past_events=past_events)
                if similar_current_events is not None:
                    similar_current_events = similar_current_events[:10]

            # upcoming events
            upcoming_events = all_events.order_by('-start_time').values()[:10]

        return render(request, 'home.html', {'tag_events': personalized_tag_events, 'department_events': personalized_departments, 'registered_events': all_registered_events, 'upcoming_events': upcoming_events,
                                             'similar_current': similar_current_events, 'club_week': club_of_week, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'],  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))


@api_view(['GET', 'POST'])
def profile(request):
    if request.user.is_authenticated:
        email = request.user.email
        person = User.objects.get(pk=email)
        # user_tags = User.objects.values('tag').filter(user=email)
        # user_profile = UserInterest.objects.filter(user=email)
        profile_form = ProfileForm(instance=person, initial={
            'tags': person.tags.all(), 'user_email': email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
        admin_form = AdminForm()
        if request.method == 'GET':
            if person.is_admin:
                admin_form = AdminForm(instance=Admin.objects.get(user=person.user_email), initial={
                    'organization': Admin.objects.filter(user=person.user_email).values('organization')
                })

            # return render(request, 'profile.html', {'person': User.objects.filter(pk=email).values(), 'form': profile_form, 'admin_form': admin_form})

        if request.method == 'POST':
            person = User.objects.get(pk=request.user.email)
            profile_form = ProfileForm(request.POST, instance=person)
            admin_form = AdminForm(request.POST)
            if profile_form.is_valid():
                if admin_form.is_valid() and profile_form.cleaned_data['is_admin'] == True:
                    admin = admin_form.save(commit=False)
                    admin.user = User.objects.get(pk=request.user.email)
                    admin = admin.save()
                # profile.user = request.user
                profile_form.save()

                return HttpResponseRedirect(reverse('real_homepage'))

        return render(request, 'profile.html', {'form': profile_form, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'], 'admin_form': admin_form,  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))


@api_view(['GET', 'POST'])
def signup(request):

    email = request.user.email
    if User.objects.filter(pk=email).exists():
        return HttpResponseRedirect(reverse('real_homepage'))

    # if request.method == 'GET':
    user_form = ProfileForm(initial={
        'user_email': email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
    admin_form = AdminForm()

    if request.method == 'POST':
        user_form = ProfileForm(request.POST)
        admin_form = AdminForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            if admin_form.is_valid() and user_form.cleaned_data['is_admin'] == True:
                admin = admin_form.save(commit=False)
                admin.user = User.objects.get(pk=request.user.email)
                admin = admin.save()

            return HttpResponseRedirect(reverse('real_homepage'))

    return render(request, 'signup.html', {'form': user_form, 'admin_form': admin_form})
    # return HttpResponseRedirect(reverse('signup'))


@api_view(['GET', 'POST'])
def event(request, event_id):
    if request.user.is_authenticated:
        # if request.method == 'GET':
        try:
            event = Event.objects.filter(pk=event_id).values()[0]
        except:
            return HttpResponseRedirect(reverse('all_events'))
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

        event['slots'] = -1 if event['attendance_limit'] is None else event['attendance_limit'] - event['attendees']

        all_events = Event.objects.filter(
            end_time__gt=datetime.date.today()).values()
        # print(event)

        similar_values = []
        for eve in all_events:
            new_event = Event.objects.get(pk=eve['event_id'])
            eve_tags = new_event.tags.all().values_list(flat=True)

            if len(eve_tags) > 0:
                if len(set(list(current_tags) + (list(eve_tags)))) < len(eve_tags) + len(current_tags) and eve['event_id'] != event_id:
                    similar_values.append(eve)

        similar_values = extra_event_params(similar_values)

        club = Organization.objects.filter(
            pk=event['organization_id']).values()

        location = Location.objects.filter(pk=event['location_id']).values()
        registered = Registration.objects.filter(
            user_email=request.user.email, event=event_id).exists()
        # print(registered)
        person = User.objects.filter(pk=request.user.email).values()[0]
        ended = Event.objects.filter(
            pk=event_id, end_time__gt=datetime.date.today())

        if request.method == 'POST':
            if request.POST.get('register'):
                if Registration.objects.filter(
                        user_email=request.user.email, event=event_id).exists() == False:
                    Registration.objects.create(
                        user_email=User.objects.get(pk=request.user.email), event=Event.objects.get(pk=event_id))
                    person = User.objects.get(pk=request.user.email)
                    person.funds = person.funds - event['fees']
                    person.save()
                else:
                    Registration.objects.filter(
                        user_email=request.user.email, event=event_id).delete()
                    person = User.objects.get(pk=request.user.email)
                    person.funds = person.funds + event['fees']
                    person.save()

            return HttpResponseRedirect(reverse('event', args=[event_id]))

        return render(request, 'event.html', {'event': event, 'ended': bool(len(ended) == 0), 'event_tags': current_tags, 'similar_events': similar_values[:3], 'club': club[0], 'location': location[0], 'registered': registered, 'is_admin': person['is_admin'], 'user_funds': person['funds'], 'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))


def club(request, cid):
    if request.user.is_authenticated:

        if request.method == 'GET':
            try:
                club = Organization.objects.filter(pk=cid).values()
            except:
                return HttpResponseRedirect(reverse('homepage'))
            if club.exists() == False:
                return HttpResponse('Some Error has occured')

            all_club_events = Event.objects.filter(
                organization=cid, end_time__gt=datetime.date.today()).order_by('-start_time').values()

            for event in all_club_events:
                event['club_name'] = Organization.objects.values(
                    'name').filter(id=event['organization_id'])[0]['name']
                event['time'] = datetime_to_string(
                    event['start_time'], event['end_time'])
                event['attendance'] = Registration.objects.filter(
                    event=event['event_id']).count()

            location = Location.objects.filter(
                location_id=club[0]['location_id']).values()

            return render(request, 'club.html', {'club': club[0], 'events': all_club_events[:3], 'location': location[0], 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'],  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('clubs'))


@api_view(['GET'])
def user_events(request):

    if request.user.is_authenticated:
        email = request.user.email

        if request.method == 'GET':
            all_registered = Registration.objects.filter(
                user_email=email).values()
            departments = Department.objects.all()
            tags = Tag.objects.all()
            user_tag = request.GET.get('tag')

            all_events = [Event.objects.filter(
                pk=reg['event_id'], end_time__gt=datetime.date.today()).values()[0] for reg in all_registered]

            try:
                past_events = [Event.objects.filter(
                    pk=reg['event_id'], end_time__lte=datetime.date.today()).values()[0] for reg in all_registered]
            except:
                past_events = None

            if user_tag:
                new_events = []

                for event in all_events:
                    new_event = Event.objects.get(pk=event['event_id'])
                    if new_event.tags.exists() and user_tag in new_event.tags.values_list(flat=True):
                        new_events.append(event)
                all_events = new_events

            all_events = extra_event_params(all_events)

        return render(request, 'registered.html', {'events': all_events, 'past_events': past_events, 'departments': departments, 'tags': tags, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'],  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))


@api_view(['GET', 'POST'])
def all_clubs(request):
    if request.user.is_authenticated:
        all_clubs = Organization.objects.all()
        search_word = None
        if request.method == 'GET':
            search_word = request.GET.get('search')
            if search_word:
                results = Organization.objects.filter(Q(name__contains=search_word) | Q(
                    description__contains=search_word)).values()

            for club in all_clubs.values():
                club['description'] = ' '.join(
                    club['description'].split(' ')[:10])

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
        return render(request, 'all_clubs.html', {'search': results, 'clubs': all_clubs, 'departments': departments, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'],  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))


@api_view(['GET', 'POST'])
def all_events(request):

    if request.user.is_authenticated:
        # if request.method == 'GET':
        search_word = request.GET.get('search')
        if search_word:
            results = Event.objects.filter(Q(event_name__contains=search_word) | Q(
                description__contains=search_word), end_time__gt=datetime.date.today()).values()
        user_tag = request.GET.get('tag')
        all_events = Event.objects.filter(
            end_time__gt=datetime.date.today()).order_by('-start_time').values()

        if user_tag:
            new_events = []

            for event in all_events:
                new_event = Event.objects.get(pk=event['event_id'])
                if new_event.tags.exists() and {'name': user_tag} in new_event.tags.all().values():
                    new_events.append(event)
            all_events = new_events

        if request.method == 'POST':
            sort = request.POST.get('sort', 1)
            dept = request.POST.get('dept', None)
            minPrice = request.POST.get('min_price', None)
            maxPrice = request.POST.get('max_price', None)
            start_date = request.POST.get('start_date', None)
            end_date = request.POST.get('end_date', None)
            # selected_tags = request.POST.get('selectedTags', None)
            selected_tags = request.POST.getlist('tagList', None)

            sorter = '-start_time' if sort == 1 else 'start_time'
            # print('selected: ', selected_tags)
            all_events = Event.objects.filter(
                end_time__gt=datetime.date.today()).order_by(sorter).values()

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
                # tags = selected_tags.split(',')
                # print(tags)

                all_events = Event.objects.filter(
                    tags__in=selected_tags, end_time__gt=datetime.date.today()).distinct().values()

        if search_word:
            results = extra_event_params(results)
        all_events = extra_event_params(all_events)

        if not search_word:
            results = None
        # print(results)
        # return redirect(reverse('all_events') )
        departments = Department.objects.all()
        all_tags = Tag.objects.all()
        return render(request, 'all_events.html', {'events': all_events, 'departments': departments, 'tags': all_tags, 'is_admin': User.objects.filter(pk=request.user.email).values()[0]['is_admin'], 'search': results,  'funds': User.objects.filter(pk=request.user.email).values()[0]['funds']})

    return HttpResponseRedirect(reverse('homepage'))

# search page


@api_view(['GET', 'POST'])
def search_page(request):
    if request.user.is_authenticated:
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

    return HttpResponseRedirect(reverse('homepage'))


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
        event['tag_list'] = new_event.tags.all().values_list(flat=True)

    return events
