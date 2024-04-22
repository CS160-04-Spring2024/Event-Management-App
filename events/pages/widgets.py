from django.forms.widgets import DateTimeInput


class DatePickerInput(DateTimeInput):
    input_type = 'datetime-local'
