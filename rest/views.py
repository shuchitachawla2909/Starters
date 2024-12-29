from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant

def home(request):
    restaurants=Restaurant.objects.all()
    context={
        'restaurants':restaurants
    }
    return render(request, 'rest/index.html',context)

def restaurants(request):
    context={
        'restaurants':Restaurant.objects.all
             }
    return render(request, 'rest/restaurants.html',context)
