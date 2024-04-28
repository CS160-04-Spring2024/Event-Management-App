from django.forms.widgets import DateTimeInput, Select


class DatePickerInput(DateTimeInput):
    input_type = 'datetime-local'


# class OrgInput(Select):
