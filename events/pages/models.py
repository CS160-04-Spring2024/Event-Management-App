from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# from tinymce import models as tinymce_models
# from django_quill.fields import QuillField
from ckeditor.fields import RichTextField


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.name


class User(models.Model):
    user_email = models.TextField(primary_key=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)  # 'student' or 'professor'
    major = models.CharField(max_length=255, null=True)
    department = models.ForeignKey('Department', on_delete=models.DO_NOTHING)
    funds = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)])
    is_admin = models.BooleanField(default=False)


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(
        'Location', on_delete=models.DO_NOTHING, blank=True, null=True)
    banner = models.URLField(blank=True, null=True)
    club_logo = models.URLField(blank=True, null=True)

    # socials - email and linkedin
    email = models.EmailField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    fees = models.DecimalField(max_digits=6, decimal_places=2)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_interest'
        unique_together = (('user', 'tag'),)


class Admin(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)

    class Meta:
        db_table = 'admin'
        unique_together = (('user', 'organization'))


class Registration(models.Model):
    user_email = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)

    class Meta:
        db_table = 'registration'
        unique_together = (('user_email', 'event'))


class EventTag(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_tag'
        unique_together = (('event', 'tag'))


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    building_name = models.CharField(max_length=255)
    room_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    image = models.URLField()


class Major(models.Model):
    major_name = models.TextField(primary_key=True)

    def __str__(self):
        return self.major_name
# class Event(models.Model):
#     content = RichTextField()
# Create your models here.
