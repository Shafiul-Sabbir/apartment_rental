from django.shortcuts import render, redirect, get_object_or_404
from .models import Apartment, Tenant
from .forms import ApartmentForm, TenantForm
from django.utils import timezone
from django.contrib import messages
# Create your views here.


def update_apartment_status():
    """Update the is_booked status of apartments based on current time."""
    now = timezone.now()+ timezone.timedelta(hours=6, minutes=0)
    Apartment.objects.update(is_booked=False)  # Reset all apartments to unbooked
    Apartment.objects.filter(tenant__move_in_date__lte=now, tenant__move_out_date__gte=now).update(is_booked=True)


def update_tenant_status(tenant):
    """Update the tenant status based on the current date."""
    now = timezone.now() + timezone.timedelta(hours=6, minutes=0)
    if tenant.move_in_date > now:
        tenant.status = 'will_arrive'
    elif tenant.move_out_date and tenant.move_out_date < now:
        tenant.status = 'moved_out'
    else:
        tenant.status = 'living'
    tenant.save()
    update_apartment_status()


def tenant_list(request):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        tenants = Tenant.objects.all()
        for tenant in tenants:
            update_tenant_status(tenant)
        return render(request, 'tenants/tenant_list.html', {'tenants': tenants})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')


def tenant_details(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        tenant = Tenant.objects.get(id=tenant_id)
        return render(request, 'tenants/tenant_details.html', {'tenant': tenant})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

def add_tenant(request):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        if request.method == 'POST':
            form = TenantForm(request.POST)
            if form.is_valid():
                tenant = form.save()
                update_tenant_status(tenant)
                return redirect('tenant_list')
            else:
                return render(request, 'tenants/add_tenant.html', {'form': form, 'error': form.errors})
        else:
            form = TenantForm()
        return render(request, 'tenants/add_tenant.html', {'form': form})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')
    
def edit_tenant(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        tenant = get_object_or_404(Tenant, id=tenant_id)
        previous_apartment = tenant.apartment
        
        if request.method == 'POST':
            form = TenantForm(request.POST, instance=tenant)
            if form.is_valid():
                tenant = form.save()
                update_tenant_status(tenant)
                
                if previous_apartment != tenant.apartment:
                    previous_apartment.is_booked = False
                    previous_apartment.save()
                    tenant.apartment.is_booked = True
                    tenant.apartment.save()
                
                return redirect('tenant_details', tenant_id=tenant.id)
        else:
            form = TenantForm(instance=tenant)
        return render(request, 'tenants/edit_tenant.html', {'form': form, 'tenant': tenant})
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')

def delete_tenant(request, tenant_id):
    user = request.user
    if user.is_authenticated and user.is_superuser :
        tenant = get_object_or_404(Tenant, id=tenant_id)
        apartment = tenant.apartment
        tenant.delete()
        apartment.is_booked = False
        apartment.save()
        return redirect('tenant_list')
    else:
        messages.error(request, 'You have to log in as an Admin to access this page.')
        return redirect('login')