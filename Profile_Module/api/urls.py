from django.urls import path
from .views import *

urlpatterns = [
    path('register_customer/', CustomerView.as_view(), name="Register_Customer"),
]