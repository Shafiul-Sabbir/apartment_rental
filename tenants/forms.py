from django import forms
from .models import Apartment, Tenant
from django.utils import timezone

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'contact', 'apartment', 'move_in_date', 'move_out_date']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'move_out_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['apartment'].queryset = Apartment.objects.exclude(
                tenant__move_in_date__lte=timezone.now(),
                tenant__move_out_date__gte=timezone.now()).exclude(
                    id=self.instance.apartment.id)
        else:
            self.fields['apartment'].queryset = Apartment.objects.exclude(
                tenant__move_in_date__lte=timezone.now(),
                tenant__move_out_date__gte=timezone.now())
    
    def clean(self):
        cleaned_data = super().clean()
        move_in_date = cleaned_data.get('move_in_date')
        move_out_date = cleaned_data.get('move_out_date')

        if move_in_date and move_out_date and move_out_date <= move_in_date:
            self.add_error('move_out_date', 'Move-out date must be after the move-in date.')

        return cleaned_data
class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['number'] 