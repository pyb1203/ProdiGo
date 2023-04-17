from django.db import models
from django.contrib.auth.models import User
from Products_Module.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, related_name="user_orders", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=8, unique=True)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    ordered_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id} by {self.user.username}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, related_name="ordered_products", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_in_different_orders", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    ordered_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.order_id}"

    class Meta:
        verbose_name = "Product Ordered"
        verbose_name_plural = "Products Ordered"

