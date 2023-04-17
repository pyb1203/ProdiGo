from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'created_timestamp',
        'updated_timestamp',
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'category',
        'title',
        'price',
        'image_url',
        'created_timestamp',
        'updated_timestamp',
    )
