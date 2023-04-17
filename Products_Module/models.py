from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"category_name: {self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="category_of_products", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"category_name: {self.category.name}, product_name: {self.title}, price: {self.price}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


