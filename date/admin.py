from django.contrib import admin
from .models import User, Sympathy


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    list_display_links = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


@admin.register(Sympathy)
class SympathyAdmin(admin.ModelAdmin):
    list_display = ('who', 'whom', 'matching', )
    list_display_links = ('who', 'whom', 'matching', )
    search_fields = ('who', 'whom', 'matching', )
