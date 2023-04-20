from django.urls import path
from .views import *

urlpatterns = [
    path('get_categories/', CategoryView.as_view(), name="Get_Categories"),
    path('get_products/', ProductView.as_view(), name="Get_Products"),
]