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
            return redirect('tenant_list')
    else:
        form = TenantForm()
    return render(request, 'tenants/add_tenant.html', {'form': form})

def edit_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant_details', tenant_id=tenant.id)
    else:
        form = TenantForm(instance=tenant)
    return render(request, 'tenants/edit_tenant.html', {'form': form, 'tenant': tenant})

def delete_tenant(request, tenant_id):
    tenant = Tenant.objects.get(id=tenant_id)
    tenant.delete()
    return redirect('tenant_list')