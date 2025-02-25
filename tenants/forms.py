from django import forms
from .models import Apartment, Tenant
from django.utils import timezone

class TenantForm(forms.ModelForm):
    # Define the form for the Tenant model
    class Meta:
        model = Tenant  # Specify the model associated with the form
        fields = ['name', 'contact', 'apartment', 'move_in_date', 'move_out_date', 'remarks']  # Include relevant fields
        widgets = {
            # Use datetime-local input for date fields to allow user-friendly date-time selection
            'move_in_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'move_out_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        # Initialize the form and modify apartment field choices dynamically
        super().__init__(*args, **kwargs)
        now = timezone.now()  # Get the current timestamp
        apartments = Apartment.objects.all()  # Fetch all apartments from the database
        apartment_choices = []  # Initialize an empty list to store choices

        for apartment in apartments:
            # commenting apartment choosing lable for client request
            '''
            if apartment.is_booked:
                # Fetch the first tenant associated with this apartment
                tenant = Tenant.objects.filter(apartment=apartment).first()
                if tenant and tenant.move_out_date > now:
                    # If the apartment is booked, show the move-out date of the current tenant
                    label = f"Apartment {apartment.number} : (booked), will be free after {tenant.move_out_date.strftime('%d/%m/%Y, %I:%M %p')}"
                else:
                    label = f"Apartment {apartment.number} : (booked)"
            else:
                # If the apartment is free, check for any future bookings
                tenant = Tenant.objects.filter(apartment=apartment, move_in_date__gte=now).first()
                if tenant:
                    # Show the next available date if there's a future booking
                    label = f"Apartment {apartment.number} : (free) until {tenant.move_in_date.strftime('%d/%m/%Y, %I:%M %p')}"
                else:
                    # If no future booking, mark it as fully available
                    label = f"Apartment {apartment.number} : (free)"
            apartment_choices.append((apartment.id, label))  # Append choices to the list
            '''            
            apartment_choices.append((apartment.id, f"Apartment {apartment.number}"))

        # Set the choices for the apartment field in the form
        self.fields['apartment'].choices = apartment_choices
        
    def clean(self):
        # Custom validation logic for the form fields
        cleaned_data = super().clean()  # Get cleaned form data
        move_in_date = cleaned_data.get('move_in_date')
        move_out_date = cleaned_data.get('move_out_date')
        contact = cleaned_data.get('contact')
        apartment = cleaned_data.get('apartment')
        print(apartment)
        if move_in_date and move_out_date:
            # Check if the selected apartment is already booked during the given date range
            overlapping_tenants = Tenant.objects.filter(
                apartment=apartment,
                move_in_date__lt=move_out_date,
                move_out_date__gt=move_in_date
            ).exclude(id=self.instance.id)  # Exclude the current tenant if updating

            if overlapping_tenants.exists():
                # If there's an overlap, show an error
                self.add_error('apartment', f'Apartment {apartment.number} is already booked during the selected date range. Confirm the availability from Engaged Apartments page and try again.')
        
        if contact and not contact.isdigit():
            # Ensure contact contains only digits
            self.add_error('contact', 'Contact must be a valid phone number.')
        
        if move_in_date and move_out_date and move_out_date <= move_in_date:
            # Ensure move-out date is later than move-in date
            self.add_error('move_out_date', 'Move-out date must be after the move-in date.')
        
        return cleaned_data  # Return the cleaned form data
    
    
class ApartmentForm(forms.ModelForm):
    # Define the form for the Apartment model
    class Meta:
        model = Apartment  # Specify the model associated with the form
        fields = ['number']  # Include only the apartment number field
