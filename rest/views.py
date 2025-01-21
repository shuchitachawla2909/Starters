from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Restaurant, RatingReview,Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import json

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

@login_required
def add_restaurant(request):
    if request.method == "POST":
        try:
            # Get data from the form submission
            name = request.POST.get("name")
            address = request.POST.get("address")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            description = request.POST.get("description", "")
            rating = request.POST.get("rating")  # Optional rating
            review = request.POST.get("review", "")  # Optional review
            main_image = request.FILES.get("main_image") 
            review_image = request.FILES.get("review_image")
            tags = request.POST.getlist("tags")  # Get selected tags as a list

            existing_restaurant = Restaurant.objects.filter(name=name, address=address).first()
            if existing_restaurant:
                return JsonResponse({"error": "A restaurant with the same name and address already exists."}, status=400)
                
            # Validation: Make sure name and rating are provided
            if not name or not rating:
                return JsonResponse({"error": "Name and rating are required."}, status=400)
            
            # Create and save the restaurant
            restaurant = Restaurant.objects.create(
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                main_image=main_image,
                description=description,
                posted_by=request.user
            )

            # Add selected tags
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                restaurant.tags.add(tag)

            # Optionally, add a review if a rating and review are provided
            if rating:
                RatingReview.objects.create(
                    restaurant=restaurant,
                    user=request.user,
                    rating=rating,
                    review=review,
                    review_image=review_image
                )

            # Recalculate the restaurant's average rating
            restaurant.calculate_average_rating()

            # Save restaurant
            restaurant.save()

            return JsonResponse({
                'success':True,
                'message':'Restaurant added successfully',
                'redirect_url':f'/restaurant/{restaurant.id}/'
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Fetch existing tags to show in the dropdown (checkbox)
    tags = Tag.objects.all()

    return render(request, "rest/add_restaurant.html", {"tags": tags})


def restaurants_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    
    # Get all restaurants associated with this tag
    restaurants = tag.restaurants.all()

    context = {
        'tag': tag,
        'restaurants': restaurants
    }

    return render(request, 'rest/restaurants_by_tag.html', context)

# @login_required
# def add_tag(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON data
#             data = json.loads(request.body)
#             tag_name = data.get('tag_name')

#             if not tag_name:
#                 return JsonResponse({'success': False, 'message': 'Tag name is missing'})

#             # Create or get the tag
#             tag, created = Tag.objects.get_or_create(name=tag_name)

#             if created:
#                 return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'success': False, 'message': 'Tag already exists'})
#         except json.JSONDecodeError:
#             return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})

#     return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def restaurant_detail(request,pk):
    restaurant=get_object_or_404(Restaurant,pk=pk)
    reviews=restaurant.ratings.all()

    if request.method== 'POST':
        rating=request.POST.get('rating')
        review=request.POST.get('review')
        review_image = request.FILES.get('review_image')

        user_review,created=RatingReview.objects.get_or_create(
            restaurant=restaurant,user=request.user,
            defaults={'rating':rating,'review':review,'review_image': review_image}
        )
        
        if not created:
            user_review.rating=rating
            user_review.review=review
            if review_image:
                user_review.review_image = review_image
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
        review_image = request.FILES.get('review_image')
        
        # Update the review and rating
        review.rating = rating
        review.review = review_text
        if review_image:
            review.review_image = review_image
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


@login_required
def update_restaurant_image(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        main_image = request.FILES.get("main_image")
        if main_image:
            restaurant.main_image = main_image
            restaurant.save()
            return redirect('rest:restaurant_detail', pk=restaurant.id)
        
        return redirect('rest:restaurant_detail', pk=restaurant.id)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


