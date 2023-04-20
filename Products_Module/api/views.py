from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from Products_Module.models import Category, Product

# Create your views here.

class CategoryView(APIView):
    
    # API to get list of categories

    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all().values(
                'id', 
                'name'
            )
            
            context = {
                'status':'Success',
                'message':'Here are all categories!',
                'categories':categories
            }

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)
    
class ProductView(APIView):

    # API to get list of products

    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.all().values(
                'id',
                'title',
                'category__name',
                'description',     
                'price',
                'image_url'
            )
            
            context = {
                'status':'Success',
                'message':'Here are all products!',
                'products':products
            }

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)

