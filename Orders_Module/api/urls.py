from django.urls import path
from .views import *

urlpatterns = [
    path('place_order/', OrderView.as_view(), name="Place_Order"),
]