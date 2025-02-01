from django.db import models

# Create your models here.

class Apartment(models.Model):
    number = models.PositiveIntegerField(unique=True)
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Apartment {self.number}"
    
class Tenant(models.Model):
    choices = [
        ('living', 'Living'),
        ('moved_out', 'Moved Out'),
    ]
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    move_in_date = models.DateTimeField()
    move_out_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=choices, default='living')
    
    def __str__(self):
        return self.name