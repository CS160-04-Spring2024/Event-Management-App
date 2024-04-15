from django.db import models
# from tinymce import models as tinymce_models
# from django_quill.fields import QuillField
from ckeditor.fields import RichTextField


class Event(models.Model):
    content = RichTextField()
# Create your models here.

class eventPanel:
    title: str
    eventName: str
    meetingOption: str
    meetingTime: str
    meetingAttributes: list

class searchData:
    title: str
    event: str
    club: str
    department: str