from typing import Any
from django import forms
# from tinymce.widgets import TinyMCE  # type: ignore
from .models import *
from ckeditor.widgets import CKEditorWidget
import datetime
from datetime import datetime
from django.utils import timezone


# Okay we're gonna try using forms now
modes = (
    ('In-Person', "In-Person"),
    ('Online', "Online"),
    ('Hybrid', "Hybrid"),
)

user_roles = (
    (True, 'Student'),
    (False, 'Professor'),
)

user_is_admin = (
    (True, 'Is Admin'),
    (False, 'User'),
)

location_object = Location.objects.all().values()
location_items = []
for locations in location_object:
    location_items.append((Location(locations), locations['building_name']))


student_roles = (
    ('Student', 'Student'),
    ('Professor', 'Professor'),
)

department_object = Department.objects.all().values()
department = ()
for dept in department_object:
    department += (Department(dept), dept['name']),

major_object = Major.objects.all().values()
major = ()
for maj in major_object:
    # major += (Department(maj), maj['major_name']),
    major += (Major(major), maj['major_name']),


tag_objects = Tag.objects.all().values()
tags = ()
for tag in tag_objects:
    tags += (tag['name'], tag['name']),


club_object = Organization.objects.all().values()
clubs = ()
for club in club_object:
    clubs += (Organization(club), club['name']),


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

        if start_time < timezone.now():
            raise forms.ValidationError('selected start time is invalid')
        if start_time >= end_time:
            raise forms.ValidationError(
                'Start and end times are infeasible')

        tags = self.cleaned_data['tags']
        if tags is None or len(tags) < 2:
            raise forms.ValidationError('Please select at least two tags')

        return cleaned_data


class AdminForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control shadow-sm rounded-pill', 'id': 'org', 'required': False, 'hidden': True}), label='')

    class Meta:
        model = Admin
        fields = ['organization']
        widgets = {
            'organization': forms.Select(attrs={'class': 'form-control shadow-sm rounded-pill', 'id': 'org', 'required': False})
        }


class ProfileForm(forms.ModelForm):
    user_email = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-sm rounded-pill', 'readonly': True}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-sm rounded-pill', 'readonly': True}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control shadow-sm rounded-pill', 'readonly': True}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))
    major = forms.ModelChoiceField(
        queryset=Major.objects.all(), required=False, widget=forms.Select(attrs={'class': 'form-control shadow-sm rounded-pill', 'blank': True}))

    class Meta:
        model = User
        fields = ['user_email', 'first_name', 'last_name',
                  'role', 'major', 'department', 'funds', 'is_admin', 'tags']

        widgets = {
            'user_email': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'disabled': True}),
            'first_name': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'disabled': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control shadow-sm rounded-pill', 'disabled': True}),
            'role': forms.Select(choices=user_roles, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'major': forms.Select(attrs={'class': 'form-control shadow-sm rounded-pill', 'blank': True}),
            'department': forms.Select(choices=department, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'funds': forms.NumberInput(attrs={'class': 'form-control shadow-sm', 'type': 'number', 'required': True, 'default': 0.00, 'min': 0.00, 'max': 1000.00}),
            # take this out in forseeable future
            'is_admin': forms.Select(choices=user_is_admin, attrs={'class': 'form-control shadow-sm rounded-pill', 'id': 'admin_stuff'})

        }

    def clean(self) -> dict[str, Any]:
        cleaned_data = super(ProfileForm, self).clean()
        major = self.cleaned_data.get('major')
        dept = self.cleaned_data.get('department')
        email = self.cleaned_data.get('user_email')

        tags = self.cleaned_data.get('tags')

        if major and dept:
            # print(dept.name)
            if str(major.department).strip() != str(dept.name).strip():
                raise forms.ValidationError(
                    'Major must be associated with Department if selected')

        if tags is None or len(tags) < 2:
            raise forms.ValidationError('Please select at least two tags')

        if '@' not in email:
            raise forms.ValidationError('Not a valid email')

        domain = email.split('@')[1]

        if domain.strip() != 'sjsu.edu':
            raise forms.ValidationError(
                'Email must be affiliated with San Jose State')

        return cleaned_data

        # widgets = {
        #     'user_email': forms.TextInput(attrs={'default': person.email, 'required': True, 'class': 'form-control shadow-sm'}),
        #     'first_name': forms.TextInput(attrs={'default': request.user.first_name, 'required': True, 'class': 'form-control shadow-sm'}),
        #     'last_name': forms.TextInput(attrs={'default': request.user.last_name, 'required': True, 'class': 'form-control shadow-sm'}),

        # }


# class UserTagForms(forms.ModelForm):
#     tag = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))

#     class Meta:
#         model = User
#         fields = ['tag']


# class EventTagForms(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))

#     class Meta:
#         model = Event
#         fields = ['tags']
