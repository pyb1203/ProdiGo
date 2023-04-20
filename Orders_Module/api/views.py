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
    
    # API to get the details of an order

    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            order_id = request.META.get('HTTP_ORDER_ID')

            if not Order.objects.filter(order_id=order_id).exists():
                raise Exception('Order does not exist')

            else:
                order = Order.objects.get(order_id=order_id)

                if order.user == user:
                    products_in_order = ProductInOrder.objects.filter(order=order)

                    products_detail= []

                    for product_in_order in products_in_order:
                        products_detail.append(
                            {
                                'product_name':product_in_order.product.title,
                                'quantity':product_in_order.quantity,
                                'price':product_in_order.product.price
                            }
                        )

                    context = {
                        'status':'Success',
                        'message':'Here are details of an order!',
                        'order_id':order.order_id,
                        'customer_username':order.user.username,
                        'total_quantity':order.total_quantity,
                        'total_price':order.total_price,
                        'ordered_on':order.ordered_timestamp,
                        'products':products_detail
                    }

                else:
                    raise Exception('You are not authorized to view this order')

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)
    
class CustomerOrdersView(APIView):
    
    # API to get the details of all the orders of a customer

    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            orders = Order.objects.filter(user=user)

            if orders:
                orders_detail = []

                for order in orders:
                    products_in_order = ProductInOrder.objects.filter(order=order)

                    products_detail= []

                    for product_in_order in products_in_order:
                        products_detail.append(
                            {
                                'product_name':product_in_order.product.title,
                                'quantity':product_in_order.quantity,
                                'price':product_in_order.product.price
                            }
                        )

                    orders_detail.append(
                        {
                            'order_id':order.order_id,
                            'total_quantity':order.total_quantity,
                            'total_price':order.total_price,
                            'ordered_on':order.ordered_timestamp,
                            'products':products_detail
                        }
                    )

                context = {
                    'status':'Success',
                    'message':'Here are the details of all the orders of a customer!',
                    'customer_username':user.username,
                    'orders':orders_detail
                }

            else:
                raise Exception('No orders placed by this customer')

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)
    
class GetAllOrders(APIView):

    # API to get the details of all the orders

    def get(self, request, *args, **kwargs):
        try:
            orders = Order.objects.all()

            orders_detail = []

            for order in orders:
                products_in_order = ProductInOrder.objects.filter(order=order)

                products_detail= []

                for product_in_order in products_in_order:
                    products_detail.append(
                        {
                            'product_name':product_in_order.product.title,
                            'quantity':product_in_order.quantity,
                            'price':product_in_order.product.price
                        }
                    )

                orders_detail.append(
                    {
                        'order_id':order.order_id,
                        'customer_username':order.user.username,
                        'total_quantity':order.total_quantity,
                        'total_price':order.total_price,
                        'ordered_on':order.ordered_timestamp,
                        'products':products_detail
                    }
                )

            context = {
                'status':'Success',
                'message':'Here are the details of all the orders!',
                'orders':orders_detail
            }

        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

        return Response(context)


    
