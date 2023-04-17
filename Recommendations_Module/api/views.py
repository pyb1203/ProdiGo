from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from Products_Module.models import Product
from Orders_Module.models import Order, ProductInOrder

# Create your views here.

class ProductRecommendationView(APIView):

    # API to get list of recommended products

    def get(self, request, product_id, *args, **kwargs):
        try:
            if not Product.objects.filter(id=product_id).exists():
                raise Exception('Product does not exist')
            
            product = Product.objects.get(id=product_id)

            # Get the category of the given product
            
            category = product.category

            # Get all orders that contain products from the same category

            orders = Order.objects.filter(
                ordered_products__product__category=category
            ).annotate(
                product_count=Count('ordered_products')
            ).filter(
                product_count__gte=2 # Only include orders with at least 2 products
            )

            # Calculate similarity scores between the given product and products in the orders

            similarities = {}

            for order in orders:
                for product_in_order in order.ordered_products.all():
                    if product_in_order.product.id != product_id:
                        if product_in_order.product.id not in similarities:
                            similarities[product_in_order.product.id] = 0

                        similarities[product_in_order.product.id] += 1 / order.product_count

            # Rank the products by their similarity scores in descending order

            sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

            # Return the top recommended products with the highest similarity scores

            recommended_products_list = []

            for x in sorted_similarities[:10]:
                recommended_product = Product.objects.get(id=x[0])

                recommended_products_list.append(
                    {
                        'product_id':x[0],
                        'product_name':recommended_product.title
                    }
                )

            context = {
                'status':'Success',
                'message':'Here is a list of top recommended products',
                'original_product_name':product.title,
                'recommended_products':recommended_products_list
            }

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)
