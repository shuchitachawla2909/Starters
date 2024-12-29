from django.db import models
from django.utils import timezone
from django.conf import settings


class Restaurant(models.Model):
    name = models.CharField(max_length=255)  # Name of the restaurant
    address = models.TextField()  # Full address of the restaurant
    pincode = models.CharField(max_length=10, blank=True, null=True)  # PIN/ZIP code
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Contact phone number
    opening_time = models.TimeField(null=True)  # Opening time
    closing_time = models.TimeField(null=True)  # Closing time
    cuisine_type = models.CharField(max_length=255)  # Type of cuisine served
    average_cost_for_two = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True) 
    rating = models.FloatField(default=0.0)  # Average rating
    image = models.ImageField(upload_to='restaurant_images', default='restaurant_images/default-rest.png')
    description = models.TextField(blank=True, null=True) # Description about the restaurant
    date_posted=models.DateTimeField(default=timezone.now)
    posted_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_DEFAULT,default=1)

    def __str__(self):
        return self.name