from django.contrib import admin
from .models import Apartment, Tenant

# Register your models here.
admin.site.register(Apartment)
admin.site.register(Tenant)
