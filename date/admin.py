from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email',)
    list_display_links = ('name', 'last_name', 'email',)
    search_fields = ('name', 'last_name', 'email',)
