from django.urls import path
from .views import *

urlpatterns = [
    path('get_recommended_products/<int:product_id>/', ProductRecommendationView.as_view(), name="Place_Order"),
]