from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker
import random as rd
import string
from Products_Module.models import Product
from .models import Order, ProductInOrder

def generate_order_id():
    prefix = 'PG'

    base_choices = string.digits
    base = ''.join(rd.choices(base_choices, k=6))

    order_id = prefix + base

    return order_id

@transaction.atomic
def populate_orders_model():
    sid = transaction.savepoint()
    
    try:

        # Creating an instance of the faker module

        fake = Faker()

        # Populating user model with fake users data

        for _ in range(10):
            profile = fake.simple_profile()

            User.objects.create_user(
                username = profile['username'],
                first_name = profile['name'],
                email = profile['mail']
            )

        # Populating order model and product in order model with fake orders data

        users = User.objects.all()
        products = Product.objects.all()

        for _ in range(60):
            order_id = generate_order_id()

            if not Order.objects.filter(order_id=order_id).exists(): 
                order = Order.objects.create(
                    user = fake.random_element(users),
                    order_id = order_id,
                    total_quantity = fake.random_int(1, 50),
                    total_price = fake.pydecimal(left_digits=5, right_digits=2, positive=True)
                )

                for _ in range(fake.random_int(1, 10)):
                    ProductInOrder.objects.create(
                        order = order,
                        product = fake.random_element(products),
                        quantity = fake.random_int(1, 15)
                    )

        transaction.savepoint_commit(sid)

        return "Success"

    except Exception as e:
        transaction.savepoint_rollback(sid)

        return e


        
