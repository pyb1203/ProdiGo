from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'user', 
        'total_quantity', 
        'total_price',
        'ordered_timestamp',
    )

@admin.register(ProductInOrder)
class ProductInOrderAdmin(admin.ModelAdmin):
    list_display = (
        'order', 
        'product', 
        'quantity',
        'ordered_timestamp',
    )
