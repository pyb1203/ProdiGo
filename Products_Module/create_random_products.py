from faker import Faker
import faker_commerce as fc
import random as rd
from .models import Category, Product

# Populating category model with the categories present in the faker commerce module

if not Category.objects.exists():
    for category_name in fc.CATEGORIES:
        Category.objects.create(
            name = category_name
        )

# Creating an instance of the faker module

fake = Faker()

# Adding faker commerce module provider to the faker module instance providers 

fake.add_provider(fc.Provider)

# Creating a list of objects of category model

categories = Category.objects.all()
categories_list = list(categories)

# Populating product model with random products

for _ in range(30):
    Product.objects.create(
        category = rd.choice(categories_list),
        title = fake.ecommerce_name(),
        description = fake.paragraph(),
        price = fake.pydecimal(left_digits=3, right_digits=2, positive=True),
        image_url = fake.image_url()
    )

