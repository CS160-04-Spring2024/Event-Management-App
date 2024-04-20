from typing import Any
from django import forms
# from tinymce.widgets import TinyMCE  # type: ignore
from .models import *
from ckeditor.widgets import CKEditorWidget
import datetime

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
    # event_name = forms.TextInput()
    # description = forms.CharField(widget=CKEditorWidget(), required=True, min_length=1)
    # mode_of_operation = forms.ChoiceField(choices=modes)
    # start_time = forms.DateTimeField(
    #     required=True)
    # end_time = forms.DateField(required=True)
    # fees = forms.DecimalField(max_digits=6, decimal_places=2, validators=[
    #     MinValueValidator(0), MaxValueValidator(1000)], required=True)
    # event_image = forms.URLField()
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

        tag = self.cleaned_data.get('tags')
        print(tag)
        # print(datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo)
        if start_time < datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError('selected start time is invalid')

        if start_time >= end_time:
            raise forms.ValidationError(
                'Start and end times are infeasible')

        if len(tag) < 1:
            raise forms.ValidationError('Please select at least one tag')

        return cleaned_data


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['organization']
        widgets = {
            'organization': forms.Select(choices=clubs, attrs={'class': 'form-control shadow-sm rounded-pill'})
        }


class ProfileForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'class': ''}))

    class Meta:
        model = User
        fields = ['user_email', 'first_name', 'last_name',
                  'role', 'major', 'department', 'funds', 'is_admin', 'tags']

        widgets = {
            'user_email': forms.TextInput(attrs={'required': True, 'class': 'form-control shadow-sm rounded-pill'}),
            'first_name': forms.TextInput(attrs={'required': True, 'class': 'form-control shadow-sm rounded-pill'}),
            'last_name': forms.TextInput(attrs={'required': True, 'class': 'form-control shadow-sm rounded-pill'}),
            'role': forms.Select(choices=user_roles, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'major': forms.Select(choices=major, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'department': forms.Select(choices=department, attrs={'class': 'form-control shadow-sm rounded-pill'}),
            'funds': forms.NumberInput(attrs={'class': 'form-control shadow-sm', 'type': 'number', 'required': True, 'default': 0.00, 'min': 0.00, 'max': 1000.00}),
            # take this out in forseeable future
            'is_admin': forms.Select(choices=user_is_admin, attrs={'class': 'form-control shadow-sm rounded-pill'})

        }

        def clean(self):
            cleaned_data = super(ProfileForm, self).clean()
            major = self.cleaned_data.get('major')
            dept = self.cleaned_data.get('dept')
            email = self.cleaned_data.get('user_email')

            tag = self.cleaned_data.get('tag')

            if dept is not None:
                if major['department'] != dept:
                    raise forms.ValidationError(
                        'Major must be associated with Department if selected')

            if tag is None or len(tag) < 1:
                raise forms.ValidationError('Please select at least one tag')

            if email.contains('@') == False:
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
