from rest_framework import serializers
from pages.models import *


class Dept_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Org_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class Interest_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'


class Tag_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_name']


class Admin_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class Registration_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class Event_Tag_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EventTag
        fields = '__all__'


class Location_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
