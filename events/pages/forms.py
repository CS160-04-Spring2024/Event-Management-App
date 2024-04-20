from django import forms
# from tinymce.widgets import TinyMCE  # type: ignore
from .models import Event
from ckeditor.widgets import CKEditorWidget


class EventForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Event
        fields = '__all__'
        # widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}
