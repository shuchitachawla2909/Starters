from django.contrib import admin
from .models import Restaurant

# admin.site.register(Restaurant)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','rating', 'posted_by', 'date_posted')
    search_fields = ('name','address')