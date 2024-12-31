from django import forms
from .models import Restaurant, RatingReview

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'address', 'rating', 'tags', 'description', 'image']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '5'})
        }
    
    # Add any custom validation if needed
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating

class RatingReviewForm(forms.ModelForm):
    class Meta:
        model = RatingReview
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '0.1', 'min': '0', 'max': '5'})
        }
    
    # Add any custom validation if needed
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
