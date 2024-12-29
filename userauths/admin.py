from django.contrib import admin
from userauths.models import User,Profile

class UserAdmin(admin.ModelAdmin):
  list_display=['username','email','bio']
  search_fields = ['email', 'username']

admin.site.register(User,UserAdmin)
admin.site.register(Profile) 