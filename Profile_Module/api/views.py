from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.contrib.auth.models import User
import random as rd
import string

# Create your views here.

def generate_username(email_id):
    temp_username = email_id.split('@')

    size = 2
    prefix_choices = string.ascii_uppercase + string.punctuation
    suffix_choices = string.ascii_lowercase + string.punctuation

    prefix = ''.join(rd.choices(prefix_choices, k=size))
    suffix = ''.join(rd.choices(suffix_choices, k=size))
    username = prefix + temp_username[0] + suffix

    return username

class CustomerView(APIView):

    # API to register the customer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        try:
            customer_data = request.data
            name = customer_data['name']
            email_id = customer_data['email_id']
            password = customer_data['password']

            if not User.objects.filter(email=email_id).exists():
                customer = User.objects.create_user(
                    username = generate_username(email_id),
                    first_name = name,
                    email = email_id,
                    password = password
                )

                token = Token.objects.create(user=customer)

                context = {
                    'status':'Success',
                    'message':'Customer Registered Successfully',
                    'customer_username':customer.username,
                    'token':token.key
                }

                transaction.savepoint_commit(sid)

            else:
                customer = User.objects.get(email=email_id)

                token = Token.objects.get(user=customer)

                raise Exception(f'Customer already exists with token {token.key}')
            
        except Exception as e:
            context = {
                'status':'Failed!', 
                'message':str(e)
            }

            transaction.savepoint_rollback(sid)
            
        return Response(context)