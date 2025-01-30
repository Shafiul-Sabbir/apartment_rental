from django.urls import path
from .views import tenant_list, tenant_details, add_tenant, edit_tenant, delete_tenant

urlpatterns = [
    path('', tenant_list, name='tenant_list'),
    path('tenant/<int:tenant_id>/', tenant_details, name='tenant_details'),
    path('add_tenant/', add_tenant, name='add_tenant'),
    path('edit_tenant/<int:tenant_id>/', edit_tenant, name='edit_tenant'),
    path('delete_tenant/<int:tenant_id>/', delete_tenant, name='delete_tenant'),
]