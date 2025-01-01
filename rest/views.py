from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Restaurant, RatingReview
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

def home(request):
    top_restaurants = Restaurant.objects.order_by('-rating')[:6]
    
    return render(request, 'rest/index.html', {
        'restaurants': top_restaurants
    })

def restaurants(request):
    context={
        'restaurants':Restaurant.objects.all()
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
        RatingReview.objects.create(
            restaurant=restaurant,
            user=request.user,
            rating=rating,
            review=review or ""  # Use an empty string if no review is provided
        )
        
        # Recalculate the average rating
        restaurant.calculate_average_rating()


        return redirect('rest:restaurant_detail', pk=restaurant.pk)


    return render(request, "rest/add_restaurant.html")  # Use the HTML template for GET requests

@login_required
def restaurant_detail(request,pk):
    restaurant=get_object_or_404(Restaurant,pk=pk)
    reviews=restaurant.ratings.all()

    if request.method== 'POST':
        rating=request.POST.get('rating')
        review=request.POST.get('review')

        user_review,created=RatingReview.objects.get_or_create(
            restaurant=restaurant,user=request.user,
            defaults={'rating':rating,'review':review}
        )
        
        if not created:
            user_review.rating=rating
            user_review.review=review
            user_review.save()

        restaurant.calculate_average_rating()
        return redirect('rest:restaurant_detail',pk=restaurant.pk)

    context={
        'restaurant':restaurant,
        'reviews':reviews
    }
    return render(request,'rest/rest_detail.html',context)


@login_required
def update_review(request, review_id):
    review = get_object_or_404(RatingReview, pk=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        # Update the review and rating
        review.rating = rating
        review.review = review_text
        review.save()

        # Recalculate the average rating after review update
        review.restaurant.calculate_average_rating()

        return redirect('rest:restaurant_detail', pk=review.restaurant.pk)

    context = {'review': review}
    return render(request, 'rest/update_review.html', context)

@login_required
def delete_review(request, review_id):
    
    review = get_object_or_404(RatingReview, pk=review_id, user=request.user)
    
    # Delete the review
    review.delete()

    # Recalculate the average rating after review deletion
    review.restaurant.calculate_average_rating()

    return redirect('rest:restaurant_detail', pk=review.restaurant.pk)

def get_rests(request):
    payload = []  # Start with an empty payload
    
    search = request.GET.get('search', '')  # Get search query, default is empty string
    
    if search:
        # If there is a search query, filter the restaurants by name
        objs = Restaurant.objects.filter(name__icontains=search)  # Case-insensitive search
        
        # Populate the payload with the filtered results
        payload = [
            {   
                'id': obj.id,
                'name': obj.name,  
            }
            for obj in objs
        ]
        
        if not payload:
            # If no results are found, return a message in the payload
            payload = [{'message': 'No restaurants found.'}]
    
    # Return the JsonResponse with the payload
    return JsonResponse({
        'status': True,
        'payload': payload
    })

