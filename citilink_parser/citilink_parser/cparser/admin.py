from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image', 'category', )
    search_fields = ('name', 'price', 'category', )


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


