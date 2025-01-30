from django import forms
from .models import Apartment, Tenant
from django.db.models import Q
from django.utils import timezone

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'contact', 'apartment', 'move_in_date', 'move_out_date']
        widgets = {
            'move_in_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'min': timezone.now().isoformat()}),
            'move_out_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(TenantForm, self).__init__(*args, **kwargs)

        # Get all occupied apartments based on active tenancy periods
        occupied_apartments = Apartment.objects.filter(
            tenant__move_out_date__gte=timezone.now()
        ).distinct()

        if self.instance and self.instance.pk:
            # If editing, allow the tenant's current apartment but exclude others that are occupied
            self.fields['apartment'].queryset = Apartment.objects.exclude(
                Q(id__in=occupied_apartments) &
                ~Q(id=self.instance.apartment.id)  # Allow selecting current apartment
            ).distinct()
        else:
            # If adding a new tenant, exclude all currently occupied apartments
            self.fields['apartment'].queryset = Apartment.objects.exclude(
                Q(id__in=occupied_apartments)
            ).distinct()

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