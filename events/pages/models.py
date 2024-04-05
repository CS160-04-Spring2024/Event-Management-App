from django.db import models
# from tinymce import models as tinymce_models
# from django_quill.fields import QuillField
from ckeditor.fields import RichTextField


class Event(models.Model):
    content = RichTextField()
# Create your models here.
