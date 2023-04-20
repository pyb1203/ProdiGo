from __future__ import absolute_import, unicode_literals

from celery import shared_task
import datetime as dt
from Products_Module.create_random_products import populate_products_model

@shared_task(bind=True)
def create_random_products_task(start_time, end_time):

    # Check if the current time is between the start and end time

    if start_time <= dt.datetime.now().time() <= end_time:
        message = populate_products_model()

        if message == "Success":
            context = {
                'status':'Success',
                'message':'Random products created successfully'
            }

        else:
            context = {
                'status':'Failed!',
                'message':str(message)
            }
    
    else:
        context = {
            'status':'Not Performed',
            'message':f'create_random_products_task skipped at {dt.datetime.now()}'
        }

    return context