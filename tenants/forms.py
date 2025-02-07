from django import forms
from .models import Apartment, Tenant
from django.db.models import Q
from django.utils import timezone

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'contact', 'apartment', 'move_in_date', 'move_out_date']
        widgets = {
            'move_in_date': forms.DateTimeInput(attrs={'type': 'datetime-local' }),
            'move_out_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     occupied_apartments = Apartment.objects.filter(
    #         is_booked=True,
    #     ).distinct()
    #     if self.instance and self.instance.pk:
    #         self.fields['apartment'].queryset = Apartment.objects.exclude(
    #             Q(id__in=occupied_apartments) & ~Q(id=self.instance.apartment.id)
    #         ).distinct()
    #     else:
    #         self.fields['apartment'].queryset = Apartment.objects.exclude(id__in=occupied_apartments).distinct()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        apartments = Apartment.objects.all()
        apartment_choices = []

        for apartment in apartments:
            if apartment.is_booked:
                tenant = Tenant.objects.filter(apartment=apartment).first()
                if tenant and tenant.move_out_date > now:
                    label = f"Apartment {apartment.number} : (booked), will be free after {tenant.move_out_date.strftime('%d/%m/%Y, %I:%M %p')}"
                else:
                    label = f"Apartment {apartment.number} : (booked)"
            else:
                tenant = Tenant.objects.filter(apartment=apartment, move_in_date__gte=now,).first()
                
                if tenant:
                    label = f"Apartment {apartment.number} : (free) until {tenant.move_in_date.strftime('%d/%m/%Y, %I:%M %p')}"
                else:
                    label = f"Apartment {apartment.number} : (free)"
            apartment_choices.append((apartment.id, label))

        self.fields['apartment'].choices = apartment_choices
        
    def clean(self):
        cleaned_data = super().clean()
        move_in_date = cleaned_data.get('move_in_date')
        move_out_date = cleaned_data.get('move_out_date')
        contact = cleaned_data.get('contact')
        apartment = cleaned_data.get('apartment')
        
        if move_in_date and move_out_date:
            overlapping_tenants = Tenant.objects.filter(
                apartment=apartment,
                move_in_date__lt=move_out_date,
                move_out_date__gt=move_in_date
            ).exclude(id=self.instance.id)

            if overlapping_tenants.exists():
                self.add_error('apartment', 'This apartment is already booked for the specified time range.')


        
        if contact and not contact.isdigit():
            self.add_error('contact', 'Contact must be a valid phone number.')
        
        if move_in_date and move_out_date and move_out_date <= move_in_date:
            self.add_error('move_out_date', 'Move-out date must be after the move-in date.')
        
        return cleaned_data
    
    
class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['number'] 