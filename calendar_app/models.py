from django.db import models
from tenants.models import Apartment, Tenant  # Assuming your main app is "tenants"

class CalendarEvent(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.tenant.name} in Apartment {self.apartment.number}"