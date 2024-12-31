from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Restaurant, RatingReview
from django.contrib.auth.models import User
from django.conf import settings

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

def add_restaurant(request):
    if request.method == "POST":
        # Get data from the form submission
        name = request.POST.get("name")
        address = request.POST.get("address")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        tags = request.POST.get("tags")
        rating = request.POST.get("rating")
        review = request.POST.get("review")
        image = request.FILES.get("image")
        
        
        # Validation: Make sure name and rating are provided
        if not name or not rating:
            return JsonResponse({"error": "Name and rating are required."}, status=400)
        
        # Create and save the restaurant
        restaurant = Restaurant(
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
            tags=tags,
            rating=rating,
            image=image,
            posted_by=request.user
        )
        restaurant.save()
        
        # Optionally, create a review (if provided) when adding the restaurant
        if review:
            RatingReview.objects.create(
                restaurant=restaurant,
                user=request.user,
                rating=rating,
                review=review
            )
        
        return JsonResponse({"message": "Restaurant added successfully!"}, status=200)

    return render(request, "rest/add_restaurant.html")  # Use the HTML template for GET requests


def restaurant_detail(request,pk):
    restaurant=get_object_or_404(Restaurant,pk=pk)
    context={
        'restaurant':restaurant
    }
    return render(request,'rest/rest_detail.html',context)