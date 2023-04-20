from django.core.management.base import BaseCommand
from Products_Module.create_random_products import populate_products_model

class Command(BaseCommand):
    help = 'Create random products'

    def handle(self, *args, **options):

        # Execute the Python function here

        result = populate_products_model()

        if result == "Success":
            print("\nRandom products created successfully\n")

        else:
            print("\n" + result + "\n")
