from django.contrib import admin
from .models import Restaurant,RatingReview,Tag

# admin.site.register(Restaurant)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','rating', 'posted_by', 'date_posted','get_tags')
    search_fields = ('name','address')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

admin.site.register(RatingReview)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)