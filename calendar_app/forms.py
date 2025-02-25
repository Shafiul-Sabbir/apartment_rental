from django import forms
from formset.ranges import DateRangeField
from formset.ranges import DateRangePicker
from django.forms.widgets import DateInput
from .models import CalendarEvent

class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['tenant', 'apartment', 'start_date', 'end_date']
        
    