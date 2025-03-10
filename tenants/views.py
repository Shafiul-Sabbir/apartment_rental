from django.shortcuts import render, redirect, get_object_or_404
from .models import Apartment, Tenant
from .forms import ApartmentForm, TenantForm
from django.utils import timezone
from django.contrib import messages
from calendar_app.models import CalendarEvent  # Import the CalendarEvent model

# Function to update the booking status of all apartments
def update_apartment_status():
    """Update the is_booked status of apartments based on the current time."""
    now = timezone.now() + timezone.timedelta(hours=6, minutes=0)  # Adjust time to match timezone
    Apartment.objects.update(is_booked=False)  # Reset all apartments to unbooked
    
    # Mark apartments as booked if a tenant is currently staying
    Apartment.objects.filter(tenant__move_in_date__lte=now, tenant__move_out_date__gte=now).update(is_booked=True)

# Function to update tenant status based on their move-in and move-out dates
def update_tenant_status(tenant):
    """Update the tenant status based on the current date."""
    now = timezone.now() + timezone.timedelta(hours=6, minutes=0)  # Adjust time to match timezone
    
    # Determine tenant status based on their move-in and move-out dates
    if tenant.move_in_date > now:
        tenant.status = 'will_arrive'  # Tenant has not yet moved in
    elif tenant.move_out_date and tenant.move_out_date < now:
        tenant.status = 'moved_out'  # Tenant has already moved out
    else:
        tenant.status = 'living'  # Tenant is currently living in the apartment
    
    tenant.save()  # Save updated status
    update_apartment_status()  # Update apartment booking status accordingly

# View to list all tenants
def tenant_list(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:  # Ensure only admin users can access
        tenants = Tenant.objects.all().order_by('-move_in_date')  # Fetch all tenants
        
        # Update status of each tenant before displaying
        for tenant in tenants:
            update_tenant_status(tenant)
        
        return render(request, 'tenants/tenant_list.html', {'tenants': tenants})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

# View to display tenant details
def tenant_details(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        tenant = Tenant.objects.get(id=tenant_id)  # Fetch tenant by ID
        return render(request, 'tenants/tenant_details.html', {'tenant': tenant})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

# View to add a new tenant
def add_tenant(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        if request.method == 'POST':  # Check if form is submitted
            form = TenantForm(request.POST)
            if form.is_valid():
                tenant = form.save()  # Save the tenant
                update_tenant_status(tenant)  # Update status after adding
                
                # Create a CalendarEvent for the tenant's stay
                CalendarEvent.objects.create(
                    tenant=tenant,
                    apartment=tenant.apartment,
                    start_date=tenant.move_in_date,
                    end_date=tenant.move_out_date
                )
                
                return redirect('tenant_list')  # Redirect to tenant list page
            else:
                return render(request, 'tenants/add_tenant.html', {'form': form, 'error': form.errors})
        else:
            form = TenantForm()  # Render an empty form for GET request
        return render(request, 'tenants/add_tenant.html', {'form': form})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

# View to edit tenant details
def edit_tenant(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        tenant = get_object_or_404(Tenant, id=tenant_id)  # Fetch tenant or return 404 if not found
        previous_apartment = tenant.apartment  # Store current apartment before updating
        
        if request.method == 'POST':
            form = TenantForm(request.POST, instance=tenant)  # Bind form to existing tenant
            if form.is_valid():
                tenant = form.save()  # Save the updated tenant details
                update_tenant_status(tenant)  # Update tenant status
                
                # If tenant's apartment changed, update both previous and new apartment booking status
                if previous_apartment != tenant.apartment:
                    previous_apartment.is_booked = False
                    previous_apartment.save()
                    tenant.apartment.is_booked = True
                    tenant.apartment.save()
                
                return redirect('tenant_details', tenant_id=tenant.id)  # Redirect to updated tenant details page
        else:
            form = TenantForm(instance=tenant)  # Pre-fill form with existing tenant details
        
        return render(request, 'tenants/edit_tenant.html', {'form': form, 'tenant': tenant})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

# View to delete a tenant
def delete_tenant(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        tenant = get_object_or_404(Tenant, id=tenant_id)  # Fetch tenant or return 404 if not found
        apartment = tenant.apartment  # Get associated apartment
        tenant.delete()  # Delete tenant record
        
        # Mark the apartment as available after tenant removal
        apartment.is_booked = False
        apartment.save()
        
        return redirect('tenant_list')  # Redirect to tenant list page
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')