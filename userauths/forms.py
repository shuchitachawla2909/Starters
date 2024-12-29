from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User,Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class UserRegisterForm(UserCreationForm):
  email=forms.EmailField()
  
  class Meta:
    model=User
    fields=['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','bio']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']

