from django.urls import path
from .views import *

urlpatterns = [
    path('place_order/', OrderView.as_view(), name="Place_Order"),
    path('get_order_details/', OrderView.as_view(), name="Get_Order_Details"),
    path('get_customer_orders/', CustomerOrdersView.as_view(), name="Get_Customer_Orders"),
    path('get_all_orders/', GetAllOrders.as_view(), name="Get_All_Orders"),
]