from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
  email=models.EmailField(unique=True,null=False)
  username=models.CharField(max_length=100,unique=True)
  bio=models.CharField(max_length=150,blank=True)

  USERNAME_FIELD="email"
  REQUIRED_FIELDS=['username']

  def __str__(self):
    return self.email
  

class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  image=models.ImageField(default='profile_pics/pink.jpg',upload_to='profile_pics')

  def __str__(self):
    return f'{self.user.username} Profile'
  
  def save(self):
    super().save()

    img=Image.open(self.image.path)

    if img.height>300 or img.width >300:
        output_size=(300,300)
        img.thumbnail(output_size)
        img.save(self.image.path)
  

