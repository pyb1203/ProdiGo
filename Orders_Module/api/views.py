from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
import ast
from Products_Module.models import Product
from Orders_Module.place_random_orders import generate_order_id
from Orders_Module.models import Order, ProductInOrder

# Create your views here.

class OrderView(APIView):

    # API to place an order

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            user = request.user

            order_data = request.data
            product_ids_list = ast.literal_eval(order_data['products'])
            products_quantity_list = ast.literal_eval(order_data['quantities'])

            products = Product.objects.filter(id__in=product_ids_list)

            while True:
                order_id = generate_order_id()
                if not Order.objects.filter(order_id=order_id).exists():
                    break

            order = Order.objects.create(
                user = user,
                order_id = order_id
            )

            ind = 0
            total_quantity = 0
            total_price = 0

            for product in products:
                ProductInOrder.objects.create(
                    order = order,
                    product = product,
                    quantity = products_quantity_list[ind]
                )

                total_quantity += products_quantity_list[ind]
                total_price += (products_quantity_list[ind] * product.price)
                
                ind += 1

            order.total_quantity = total_quantity
            order.total_price = total_price
            order.save(
                update_fields=[
                    'total_quantity',
                    'total_price'
                ]
            )
            
            context = {
                'status':'Success',
                'message':'Order Placed Successfully',
                'order_id':order.order_id,
                'customer_username':user.username
            }

            transaction.savepoint_commit(sid)

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

            transaction.savepoint_rollback(sid)
            
        return Response(context)