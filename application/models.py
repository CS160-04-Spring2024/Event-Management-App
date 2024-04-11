from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=255)
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)  # 'student' or 'professor'
    major = models.CharField(max_length=255, null=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

class Organization(models.Model):
    organization_name = models.CharField(max_length=255)

class Event(models.Model):
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

class UserInterest(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

class Admin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

class Registration(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

class EventTag(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

class Location(models.Model):
    building_name = models.CharField(max_length=255)
    room_number = models.CharField(max_length=50)
    address = models.TextField()
    image = models.URLField() 
