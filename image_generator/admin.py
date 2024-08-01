from django.contrib import admin
from .models import User 

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'original_photo', 'prompted_photo')
    search_fields = ('first_name', 'last_name')

