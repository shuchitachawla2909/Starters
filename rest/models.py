from django.db import models
from django.utils import timezone
from django.conf import settings
from geopy.distance import geodesic
import requests

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)  
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)  # Rating can be 1 to 5
    distance = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  # Latitude from Geoapify API
    longitude = models.FloatField(null=True, blank=True)  # Longitude from Geoapify API
    tags = models.CharField(max_length=255, blank=True)  # You can use a TextField for multiple tags or a ManyToMany field
    image = models.ImageField(upload_to='restaurant_images', default='restaurant_images/default-rest.png',blank=True,null=True)
    description = models.TextField(blank=True, null=True) # Description about the restaurant
    date_posted=models.DateTimeField(default=timezone.now)
    posted_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_DEFAULT,default=1)

    def __str__(self):
        return self.name
    
    def calculate_average_rating(self):
        ratings = self.ratings.all()
        average = sum(r.rating for r in ratings) / ratings.count() if ratings.exists() else 0
        self.rating = average
        self.save()
    

    def calculate_distance(self, college_lat, college_lon):
        if self.latitude and self.longitude:
            restaurant_coords = (self.latitude, self.longitude)
            college_coords = (college_lat, college_lon)
            return geodesic(restaurant_coords, college_coords).kilometers
        return None

    def save(self, *args, **kwargs):
        # Define college coordinates (static or dynamic)
        college_lat = 25.2623  # College Latitude
        college_lon = 82.9893  # College Longitude

        # Calculate the distance if latitude and longitude are provided
        if self.latitude and self.longitude:
            self.distance = self.calculate_distance(college_lat, college_lon)

        # Save the restaurant with the distance calculated
        super().save(*args, **kwargs)


class RatingReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    review = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('restaurant', 'user')  # Ensure each user can rate only once

    def __str__(self):
        return f"{self.user} rated {self.restaurant.name} with {self.rating}"



    