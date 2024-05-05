from pages.models import *
from typing import Any
from django import forms
from django.utils import timezone

modes = (
    ('In-Person', "In-Person"),
    ('Online', "Online"),
    ('Hybrid', "Hybrid"),
)

location_object = Location.objects.all().values()
location_items = []
for locations in location_object:
    location_items.append((Location(locations), locations['building_name']))


department_object = Department.objects.all().values()
department = ()
for dept in department_object:
    department += (Department(dept), dept['name']),

major_object = Major.objects.all().values()
major = ()
for maj in major_object:
    # major += (Department(maj), maj['major_name']),
    major += (Major(major), maj['major_name']),


class EventForm(forms.ModelForm):

    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control shadow-sm '}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))

    class Meta:
        model = Event
        fields = ['event_name', 'description', 'mode_of_operation',
                  'start_time', 'end_time', 'fees', 'event_image', 'location', 'tags']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'required': True}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'type': 'datetime-local', 'required': True}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'type': 'datetime-local', 'required': True}),
            'mode_of_operation': forms.Select(choices=modes, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control shadow-sm', 'type': 'number', 'required': True, 'default': 0.00, 'min': 0.00, 'max': 1000.00}),
            'description': forms.Textarea(attrs={'rows': 10, 'class': 'form-control shadow-sm', 'required': True, 'minlength': 3}),
            # 'location': forms.Select(choices=location, attrs={'class': 'form-control shadow-sm'}),
            'event_image': forms.URLInput(attrs={'class': 'form-control shadow-sm'})
        }

        # widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

    def clean(self) -> dict[str, Any]:
        cleaned_data = super(EventForm, self).clean()

        start_time = self.cleaned_data.get('start_time')
        end_time = self.cleaned_data.get('end_time')

        tags = self.cleaned_data.get('tags')
        # print(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
        if end_time < timezone.now():
            raise forms.ValidationError('selected end time is invalid')

        if start_time >= end_time:
            raise forms.ValidationError(
                'Start and end times are infeasible')

        if tags is None or len(tags) < 2:
            raise forms.ValidationError('Please select at least two tags')

        return cleaned_data


class EventEditForm(forms.ModelForm):

    location = forms.ModelChoiceField(queryset=Location.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control shadow-sm '}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))

    class Meta:
        model = Event
        fields = ['event_name', 'description', 'mode_of_operation',
                  'start_time', 'end_time', 'fees', 'event_image', 'location', 'tags']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'required': True}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'type': 'datetime-local', 'required': True}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'type': 'datetime-local', 'required': True}),
            'mode_of_operation': forms.Select(choices=modes, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'fees': forms.NumberInput(attrs={'class': 'form-control shadow-sm', 'type': 'number', 'required': True, 'default': 0.00, 'min': 0.00, 'max': 1000.00}),
            'description': forms.Textarea(attrs={'rows': 10, 'class': 'form-control shadow-sm', 'required': True, 'minlength': 3}),
            'event_image': forms.URLInput(attrs={'class': 'form-control shadow-sm'})
        }

    def clean(self):
        cleaned_data = super(EventEditForm, self).clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        tags = cleaned_data.get('tags')

        if end_time < timezone.now():
            raise forms.ValidationError('Selected end time is invalid')

        if start_time >= end_time:
            raise forms.ValidationError('Start and end times are infeasible')

        if tags is None or len(tags) < 2:
            raise forms.ValidationError('Please select at least two tags')

        return cleaned_data