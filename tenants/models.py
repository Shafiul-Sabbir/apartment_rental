from django.db import models

# Create your models here.

class Apartment(models.Model):
    number = models.PositiveIntegerField(unique=True)
    
    def __str__(self):
        return f"Apartment {self.number}"
    
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    move_in_date = models.DateField()
    move_out_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
