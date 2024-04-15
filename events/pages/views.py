from django.shortcuts import render
from .forms import EventForm
from .models import eventPanel, searchData
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

# card: title(), subtitle, actual event name, meeting option, meeting time, more info about event
tempData = {'val2':['Comp Prog', "ICPC Intro Session 2", "In person", "Mon 6:00pm - 7:15pm", "SWE"]}

def user_registered_events(request): # render user registered event page
    # eventPanel class is in models.py
    # used to store events as objects to display on template
    event1 = eventPanel()
    event1.title = 'Comp Prog'
    event1.eventName = 'ICPC Intro Session'
    event1.meetingOption = 'In person'
    event1.meetingTime = 'Mon 6:00pm - 7:15pm'
    event1.meetingAttributes = ["SWE", "CS", "CE"]

    event2 = eventPanel()
    event2.title = 'CS160 - Team 6'
    event2.eventName = 'Project Meeting'
    event2.meetingOption = 'Hybrid: In person/Discord'
    event2.meetingTime = 'Friday - All Day'
    event2.meetingAttributes = ["SWE", "CS"]

    events = [event1, event2]

    return render(request, 'user_registered_events.html', {'events': events})

def search_results(request): # render user's query {events, clubs, departments}
    # searchData class is in models.py
    # used to store results as objects to display on template
    # example of a user searching the SJSU gaming club
    title = searchData() # display search keyword on template
    title.title = 'SJSU Gaming'

    # actual search results/queries
    # search0 = searchData()
    # search0.title = 'SJSU Gaming Club Page'
    # search0.club = 'SJSU Gaming Club'

    search1 = searchData()
    search1.title = 'In-house Meeting'
    search1.event = 'SJSU Valorant Tournament'
    search1.club = 'SJSU Gaming Club'

    search2 = searchData()
    search2.title = 'In-house Meeting'
    search2.event = 'SJSU League of Legends Tournament'
    search2.club = 'SJSU Gaming Club'

    search3 = searchData()
    search3.title = 'Social Meeting'
    search3.event = 'SJSU Movie Night: Dungeons and Dragons'
    search3.club = 'SJSU Gaming Club'

    searchResults =[search1, search2, search3]

    return render(request, 'search_results.html', {'title' : title, 'results' : searchResults})

def all_events(request):
    return render(request, 'all_events.html', {})
