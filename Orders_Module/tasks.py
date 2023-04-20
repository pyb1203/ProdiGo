from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime as dt
from Orders_Module.place_random_orders import populate_orders_model

@shared_task(bind=True)
def place_random_orders_task(self, start_time, end_time):

    # Check if the current time is between the start and end time

    if start_time <= dt.datetime.now().time() <= end_time:
        message = populate_orders_model()

        if message == "Success":
            context = {
                'status':'Success',
                'message':'Random orders placed successfully'
            }

        else:
            context = {
                'status':'Failed!',
                'message':str(message)
            }

    else:
        context = {
            'status':'Not Performed',
            'message':f'place_random_orders_task skipped at {dt.datetime.now()}'
        }

    return context