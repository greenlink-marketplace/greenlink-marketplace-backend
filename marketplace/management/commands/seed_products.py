from django.core.management.base import BaseCommand
from marketplace.models import Product, ProductCategory, Company
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Populates the database with dummy data for Company, ProductCategory and Product'

    def handle(self, *args, **kwargs):
        companies_objs = Company.objects.all()
        products_categories_objs = ProductCategory.objects.all()
        
        # Create products
        for _ in range(30):
            name_product = fake.word().capitalize()
            while Product.objects.filter(name=name_product).exists():
                name_product = fake.word().capitalize()
            
            Product.objects.create(
                company=random.choice(companies_objs),
                category=random.choice(products_categories_objs),
                name=name_product,
                description=fake.text(max_nb_chars=100),
                price_cents=random.randint(500, 20000),  # R$5,00 to R$200,00
                quantity=random.randint(1, 20),
                purchase_contact=fake.email(),
                is_active=True,
                is_sustainable=random.choice([True, False]),
            )

        self.stdout.write(
            self.style.SUCCESS(
                "✅ Database populated with fictitious products."
            )
        )
