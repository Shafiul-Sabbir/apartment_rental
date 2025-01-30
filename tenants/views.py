from django.shortcuts import render, redirect
from .models import Apartment, Tenant
from .forms import ApartmentForm, TenantForm
from django.utils import timezone
# Create your views here.

def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenants/tenant_list.html', {'tenants': tenants})

def tenant_details(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    return render(request, 'tenants/tenant_details.html', {'tenant': tenant})

def add_tenant(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            Apartment.objects.filter(id=form.cleaned_data['apartment'].id).update(is_booked=True)
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'tenants/add_tenant.html', {'form': form})

def edit_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    previous_apartment = tenant.apartment
    
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            # tenant = form.save(commit=False)
            tenant = form.save()
            if tenant.move_out_date and tenant.move_out_date < timezone.now():
                tenant.status = 'moved_out'
            else:
                tenant.status = 'living'
            tenant.save()
            # Update the is_booked status of the previous apartment
            previous_apartment.is_booked = False
            previous_apartment.save()
            # Update the is_booked status of the new apartment
            Apartment.objects.filter(id=form.cleaned_data['apartment'].id).update(is_booked=True)
            
            return redirect('tenant_details', tenant_id=tenant.id)
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'tenants/edit_tenant.html', {'form': form, 'tenant': tenant})

def delete_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    apartment = tenant.apartment
    tenant.delete()
    apartment.is_booked = False
    apartment.save()
    return redirect('tenant_list')