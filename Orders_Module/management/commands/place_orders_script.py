from django.core.management.base import BaseCommand
from Orders_Module.place_random_orders import populate_orders_model

class Command(BaseCommand):
    help = 'Place random orders'

    def handle(self, *args, **options):

        # Execute the Python function here

        result = populate_orders_model()

        if result == "Success":
            print("\nRandom orders placed successfully\n")

        else:
            print("\n" + result + "\n")
