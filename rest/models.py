from django.db import models

class Restaurant(models.Model):
  title=models.CharField(max_length=100)
  
